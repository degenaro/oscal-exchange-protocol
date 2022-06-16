# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2022 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""OSCAL Exchange Protocol."""
import logging
import logging.config
import pathlib
import sys
import tempfile
import uuid
from typing import List, Union

from db import Db

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from helper import helper

import trestle.core.models.elements as elements
from trestle.oscal.profile import Profile
from trestle.oscal.ssp import SystemSecurityPlan

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
depends = Depends()
depends_scheme = Depends(oauth2_scheme)

logging.getLogger('uvicorn.error').propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='OSCAL Exchange Protocol (OXP)',
    description='The OSCAL Exchange Protocol API',
    version=helper.get_version(),
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
)

db = Db(logger)

profile_phase_i = helper.get_profile_phase_i()
ssp_phase_i = helper.get_ssp_phase_i()
ssp_phase_ii = helper.get_ssp_phase_ii()


def str_to_obj(oscal_str, obm_type):
    """Transform string to object."""
    # save in temp file
    temp_path = pathlib.Path(tempfile.gettempdir()) / 'oscal.json'
    with open(temp_path, 'w') as f:
        f.write(oscal_str)
    # validate
    oscal = obm_type.oscal_read(temp_path)
    return oscal


# Authentication
@app.post('/token', include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = depends):
    """Authenticate user."""
    token = str(uuid.uuid4())
    return {'access_token': token, 'token_type': 'bearer'}


# CATALOGS


@app.post(
    '/catalogs', tags=['Lifecycle: Catalogs'], response_model=str, description='Add an OSCAL catalog in datastore.'
)
async def add_catalog(catalog: UploadFile, token: str = depends_scheme):
    """Add OSCAL catalog."""
    oscal_path = 'catalog'
    oscal_file = catalog
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # add into db
    result = db.add_catalog(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/catalogs/catalog-id',
    tags=['Lifecycle: Catalogs'],
    response_model=str,
    description='Replace an OSCAL catalog in datastore.'
)
async def replace_catalog(catalog_id: str, catalog: UploadFile, token: str = depends_scheme):
    """Replace OSCAL catalog."""
    oscal_path = 'catalog'
    oscal_file = catalog
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_catalog(catalog_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {catalog_id}')
    # success!
    return result


@app.delete(
    '/catalogs/catalog-id',
    tags=['Lifecycle: Catalogs'],
    response_model=str,
    description='Delete an OSCAL catalog from datastore.'
)
async def delete_catalog(catalog_id: str, token: str = depends_scheme):
    """Delete OSCAL catalog."""
    # get from db
    result = db.delete_catalog(catalog_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {catalog_id}')
    # success!
    return result


@app.get(
    '/catalogs/id-list',
    tags=['Lifecycle: Catalogs'],
    response_model=str,
    description='Get list OSCAL catalog ids from datastore.'
)
async def get_catalog_id_list():
    """Retrieve OSCAL catalog ids."""
    # get from db
    result = db.get_catalog_id_list()
    # success!
    return result


@app.get(
    '/catalogs/catalog-id',
    tags=['Lifecycle: Catalogs'],
    response_model=str,
    description='Get an OSCAL catalog from datastore.'
)
async def get_catalog(catalog_id: str):
    """Retrieve OSCAL catalog."""
    # get from db
    result = db.get_catalog(catalog_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {catalog_id}')
    # success!
    return result


# PROFILES


@app.post(
    '/profiles', tags=['Lifecycle: Profiles'], response_model=str, description='Add an OSCAL profile in datastore.'
)
async def add_profile(profile: UploadFile, token: str = depends_scheme):
    """Add OSCAL profile."""
    oscal_path = 'profile'
    oscal_file = profile
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # extract profile_mnemonic
    key = helper.get_profile_mnemonic()
    try:
        for prop in oscal.metadata.props:
            if prop.name == key:
                profile_mnemonic = prop.value
                break
    except Exception:
        profile_mnemonic = None
    # add into db
    result = db.add_profile(oscal.uuid, oscal.oscal_serialize_json(), profile_mnemonic)
    # success!
    return result


@app.put(
    '/profiles/profile-id',
    tags=['Lifecycle: Profiles'],
    response_model=str,
    description='Replace an OSCAL profile in datastore.'
)
async def replace_profile(profile_id: str, profile: UploadFile, token: str = depends_scheme):
    """Replace OSCAL profile."""
    oscal_path = 'profile'
    oscal_file = profile
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_profile(profile_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {profile_id}')
    # success!
    return result


@app.delete(
    '/profiles/profile-id',
    tags=['Lifecycle: Profiles'],
    response_model=str,
    description='Delete an OSCAL profile from datastore.'
)
async def delete_profile(profile_id: str, token: str = depends_scheme):
    """Delete OSCAL profile."""
    # get from db
    result = db.delete_profile(profile_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {profile_id}')
    # success!
    return result


@app.get(
    '/profiles/id-list',
    tags=['Lifecycle: Profiles'],
    response_model=str,
    description='Get list OSCAL profile ids from datastore.'
)
async def get_profile_id_list():
    """Retrieve OSCAL profile ids."""
    # get from db
    result = db.get_profile_id_list()
    # success!
    return result


@app.get(
    '/profiles/profile-id',
    tags=['Lifecycle: Profiles'],
    response_model=str,
    description='Get an OSCAL profile from datastore.'
)
async def get_profile(profile_id: str):
    """Retrieve OSCAL profile."""
    # get from db
    result = db.get_profile(profile_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {profile_id}')
    # success!
    return result


# COMPONENT_DEFINITIONS


@app.post(
    '/component-definitions',
    tags=['Lifecycle: Component Definitions'],
    response_model=str,
    description='Add an OSCAL component-definition in datastore.'
)
async def add_component_definition(component_definition: UploadFile, token: str = depends_scheme):
    """Add OSCAL component_definition."""
    oscal_path = 'component-definition'
    oscal_file = component_definition
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # put into db
    result = db.add_component_definition(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/component-definitions/component-definition-id',
    tags=['Lifecycle: Component Definitions'],
    response_model=str,
    description='Replace an OSCAL component-definition in datastore.'
)
async def replace_component_definition(
    component_definition_id: str, component_definition: UploadFile, token: str = depends_scheme
):
    """Replace OSCAL component-definition."""
    oscal_path = 'component-definition'
    oscal_file = component_definition
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_component_definition(component_definition_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {component_definition_id}')
    # success!
    return result


@app.delete(
    '/component-definitions/component-definition-id',
    tags=['Lifecycle: Component Definitions'],
    response_model=str,
    description='Delete an OSCAL component-definition from datastore.'
)
async def delete_component_definition(component_definition_id: str, token: str = depends_scheme):
    """Delete OSCAL component-definition."""
    # get from db
    result = db.delete_component_definition(component_definition_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {component_definition_id}')
    # success!
    return result


@app.get(
    '/component-definitions/id-list',
    tags=['Lifecycle: Component Definitions'],
    response_model=str,
    description='Get list OSCAL component-definition ids from datastore.'
)
async def get_component_definition_id_list():
    """Retrieve OSCAL component-definition ids."""
    # get from db
    result = db.get_component_definition_id_list()
    # success!
    return result


@app.get(
    '/component-definitions/component-definition-id',
    tags=['Lifecycle: Component Definitions'],
    response_model=str,
    description='Get an OSCAL component-definition from datastore.'
)
async def get_component_definition(component_definition_id: str):
    """Retrieve OSCAL component-definition."""
    # get from db
    result = db.get_component_definition(component_definition_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {component_definition_id}')
    # success!
    return result


# SYSTEM_SECURITY_PLANS


@app.post(
    '/system-security-plans',
    tags=['Lifecycle: System Security Plans'],
    response_model=str,
    description='Add an OSCAL system-security-plan in datastore.'
)
async def add_system_security_plan(system_security_plan: UploadFile, token: str = depends_scheme):
    """Add OSCAL system_security_plan."""
    oscal_path = 'system-security-plan'
    oscal_file = system_security_plan
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # add into db
    result = db.add_system_security_plan(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/system-security-plans/system-security-plan-id',
    tags=['Lifecycle: System Security Plans'],
    response_model=str,
    description='Replace an OSCAL system-security-plan in datastore.'
)
async def replace_system_security_plan(
    system_security_plan_id: str, system_security_plan: UploadFile, token: str = depends_scheme
):
    """Replace OSCAL system-security-plan."""
    oscal_path = 'system-security-plan'
    oscal_file = system_security_plan
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_system_security_plan(system_security_plan_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {system_security_plan_id}')
    # success!
    return result


@app.delete(
    '/system-security-plans/system-security-plan-id',
    tags=['Lifecycle: System Security Plans'],
    response_model=str,
    description='Delete an OSCAL system-security-plan from datastore.'
)
async def delete_system_security_plan(system_security_plan_id: str, token: str = depends_scheme):
    """Delete OSCAL system-security-plan."""
    # get from db
    result = db.delete_system_security_plan(system_security_plan_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {system_security_plan_id}')
    # success!
    return result


@app.get(
    '/system-security-plans/id-list',
    tags=['Lifecycle: System Security Plans'],
    response_model=str,
    description='Get list OSCAL system-security-plans ids from datastore.'
)
async def get_system_security_plan_id_list():
    """Retrieve OSCAL system-security-plans ids."""
    # get from db
    result = db.get_system_security_plan_id_list()
    # success!
    return result


@app.get(
    '/system-security-plans/system-security-plan-id',
    tags=['Lifecycle: System Security Plans'],
    response_model=str,
    description='Get an OSCAL system-security-plan from datastore.'
)
async def get_system_security_plan(system_security_plan_id: str):
    """Retrieve OSCAL system-security-plan."""
    # get from db
    result = db.get_system_security_plan(system_security_plan_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {system_security_plan_id}')
    # success!
    return result


# ASSESSMENT_PLAN


@app.post(
    '/assessment-plans',
    tags=['Lifecycle: Assessment Plans'],
    response_model=str,
    description='Add an OSCAL assessment-plan in datastore.'
)
async def add_assessment_plans(assessment_plan: UploadFile, token: str = depends_scheme):
    """Add OSCAL assessment_plan."""
    oscal_path = 'assessment-plan'
    oscal_file = assessment_plan
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # put into db
    result = db.add_assessment_plan(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/assessment-plans/assessment-plan-id',
    tags=['Lifecycle: Assessment Plans'],
    response_model=str,
    description='Replace an OSCAL assessment-plan in datastore.'
)
async def replace_assessment_plan(assessment_plan_id: str, assessment_plan: UploadFile, token: str = depends_scheme):
    """Replace OSCAL assessment-plan."""
    oscal_path = 'assessment-plan'
    oscal_file = assessment_plan
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_assessment_plan(assessment_plan_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_plan_id}')
    # success!
    return result


@app.delete(
    '/assessment-plans/assessment-plan-id',
    tags=['Lifecycle: Assessment Plans'],
    response_model=str,
    description='Delete an OSCAL assessment-plan from datastore.'
)
async def delete_assessment_plan(assessment_plan_id: str, token: str = depends_scheme):
    """Delete OSCAL assessment-plan."""
    # get from db
    result = db.delete_assessment_plan(assessment_plan_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_plan_id}')
    # success!
    return result


@app.get(
    '/assessment-plans/id-list',
    tags=['Lifecycle: Assessment Plans'],
    response_model=str,
    description='Get list OSCAL assessment-plan ids from datastore.'
)
async def get_assessment_plan_id_list():
    """Retrieve OSCAL assessment-plan ids."""
    # get from db
    result = db.get_assessment_plan_id_list()
    # success!
    return result


@app.get(
    '/assessment-plans/assessment-plan-id',
    tags=['Lifecycle: Assessment Plans'],
    response_model=str,
    description='Get an OSCAL assessment-plan from datastore.'
)
async def get_assessment_plan(assessment_plan_id: str):
    """Retrieve OSCAL assessment-plan."""
    # get from db
    result = db.get_assessment_plan(assessment_plan_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_plan_id}')
    # success!
    return result


# ASSESSMENT_RESULTS


@app.post(
    '/assessment-results',
    tags=['Lifecycle: Assessment Results'],
    response_model=str,
    description='Add an OSCAL assessment-results in datastore.'
)
async def add_assessment_results(assessment_results: UploadFile, token: str = depends_scheme):
    """Add OSCAL assessment_results."""
    oscal_path = 'assessment-results'
    oscal_file = assessment_results
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # put into db
    result = db.add_assessment_results(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/assessment-results/assessment-results-id',
    tags=['Lifecycle: Assessment Results'],
    response_model=str,
    description='Replace an OSCAL assessment-results in datastore.'
)
async def replace_assessment_results(
    assessment_results_id: str, assessment_results: UploadFile, token: str = depends_scheme
):
    """Replace OSCAL assessment-results."""
    oscal_path = 'assessment-results'
    oscal_file = assessment_results
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_assessment_results(assessment_results_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_results_id}')
    # success!
    return result


@app.delete(
    '/assessment-results/assessment-results-id',
    tags=['Lifecycle: Assessment Results'],
    response_model=str,
    description='Delete an OSCAL assessment-results from datastore.'
)
async def delete_assessment_results(assessment_results_id: str, token: str = depends_scheme):
    """Delete OSCAL assessment-results."""
    # get from db
    result = db.delete_assessment_results(assessment_results_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_results_id}')
    # success!
    return result


@app.get(
    '/assessment-results/id-list',
    tags=['Lifecycle: Assessment Results'],
    response_model=str,
    description='Get list OSCAL assessment-results ids from datastore.'
)
async def get_assessment_results_id_list():
    """Retrieve OSCAL assessment-results ids."""
    # get from db
    result = db.get_assessment_results_id_list()
    # success!
    return result


@app.get(
    '/assessment-results/assessment-results-id',
    tags=['Lifecycle: Assessment Results'],
    response_model=str,
    description='Get an OSCAL assessment-results from datastore.'
)
async def get_assessment_results(assessment_results_id: str):
    """Retrieve OSCAL assessment-results."""
    # get from db
    result = db.get_assessment_results(assessment_results_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {assessment_results_id}')
    # success!
    return result


# PLAN_OF_ACTION_AND_MILESTONES


@app.post(
    '/plan-of-action-and-milestones',
    tags=['Lifecycle: Plan of Action and Milestones'],
    response_model=str,
    description='Add an OSCAL plan-of-action-and-milestones in datastore.'
)
async def add_plan_of_action_and_milestones(plan_of_action_and_milestones: UploadFile, token: str = depends_scheme):
    """Add OSCAL plan_of_action_and_milestones."""
    oscal_path = 'plan-of-action-and-milestones'
    oscal_file = plan_of_action_and_milestones
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # add into db
    result = db.add_plan_of_action_and_milestones(oscal.uuid, oscal.oscal_serialize_json())
    # success!
    return result


@app.put(
    '/plan-of-action-and-milestones/plan-of-action-and-milestones-id',
    tags=['Lifecycle: Plan of Action and Milestones'],
    response_model=str,
    description='Replace an OSCAL plan-of-action-and-milestones in datastore.'
)
async def replace_plan_of_action_and_milestones(
    plan_of_action_and_milestones_id: str, plan_of_action_and_milestones: UploadFile, token: str = depends_scheme
):
    """Replace OSCAL plan-of-action-and-milestones."""
    oscal_path = 'plan-of-action-and-milestones'
    oscal_file = plan_of_action_and_milestones
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        raise HTTPException(status_code=400, detail=f'Invalid {oscal_path} in file.')
    # replace into db
    result = db.replace_plan_of_action_and_milestones(plan_of_action_and_milestones_id, oscal.oscal_serialize_json())
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {plan_of_action_and_milestones_id}')
    # success!
    return result


@app.delete(
    '/plan-of-action-and-milestones/plan-of-action-and-milestones-id',
    tags=['Lifecycle: Plan of Action and Milestones'],
    response_model=str,
    description='Delete an OSCAL plan-of-action-and-milestones from datastore.'
)
async def delete_plan_of_action_and_milestones(plan_of_action_and_milestones_id: str, token: str = depends_scheme):
    """Delete OSCAL plan-of-action-and-milestones."""
    # get from db
    result = db.delete_plan_of_action_and_milestones(plan_of_action_and_milestones_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {plan_of_action_and_milestones_id}')
    # success!
    return result


@app.get(
    '/plan-of-action-and-milestones/id-list',
    tags=['Lifecycle: Plan of Action and Milestones'],
    response_model=str,
    description='Get list OSCAL plan-of-action-and-milestones ids from datastore.'
)
async def get_plan_of_action_and_milestones_id_list():
    """Retrieve OSCAL plan-of-action-and-milestones ids."""
    # get from db
    result = db.get_plan_of_action_and_milestones_id_list()
    # success!
    return result


@app.get(
    '/plan-of-action-and-milestones/plan-of-action-and-milestones-id',
    tags=['Lifecycle: Plan of Action and Milestones'],
    response_model=str,
    description='Get an OSCAL plan-of-action-and-milestones from datastore.'
)
async def get_plan_of_action_and_milestones(plan_of_action_and_milestones_id: str):
    """Retrieve OSCAL plan-of-action-and-milestones."""
    # get from db
    result = db.get_plan_of_action_and_milestones(plan_of_action_and_milestones_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'Not found {plan_of_action_and_milestones_id}')
    # success!
    return result


# Validation

# ===== Validation: phase I =====


@app.post(
    '/profile/component/pvp-component-id',
    name='Policy Validation Point driven: get profiles by checks',
    tags=['Validation: phase I (profiles)'],
    response_model=List[Profile],
    description='Get list of profiles for the pvp-component.'
)
async def pvp_get_profiles(pvp_component_id: str, system_security_plan: Union[UploadFile, None] = None):
    """Get OSCAL profiles for pvp component."""
    result = []
    if system_security_plan:
        logger.debug(f'ssp: {system_security_plan}')
    # TBD: use SSP to filter profiles
    search_result = db.search_profiles(pvp_component_id)
    oscal_path = 'profile'
    # get a wrapped object
    element_path = elements.ElementPath(oscal_path)
    obm_type = element_path.get_obm_wrapped_type()
    for item in search_result:
        oscal = str_to_obj(item, obm_type)
        result.append(oscal)
    return result


@app.post(
    '/profile',
    name='Compliance Administration Center driven: put profile by checks',
    tags=['Validation: phase I (profiles)'],
    response_model=str,
    description='Put profile for the pvp-component.'
)
async def pap_put_profile(profile: Profile = profile_phase_i, token: str = depends_scheme):
    """Put OSCAL profile for pvp component."""
    # TBD
    return 'OK'


# ===== Validation: phase II =====


@app.post(
    '/system-security-plan/component/pvp-component-id',
    name='Policy Validation Point driven: get System Security Plans',
    tags=['Validation: phase II (system security plans)'],
    response_model=List[SystemSecurityPlan],
    description='Get list of system security plans for the pvp-component.'
)
async def pvp_get_system_security_plans(pvp_component_id: str, system_security_plan: Union[UploadFile, None] = None):
    """Get OSCAL system security plans for pvp component."""
    result = []
    if system_security_plan:
        logger.debug(f'ssp: {system_security_plan}')
    # TBD
    result = ssp_phase_ii
    return result


@app.post(
    '/system-security-plan',
    name='Compliance Administration Center driven: put System Security Plan',
    tags=['Validation: phase II (system security plans)'],
    response_model=str,
    description='Put system security plan for the pvp-component.'
)
async def pap_put_system_security_plan(
    system_security_plan: SystemSecurityPlan = ssp_phase_ii, token: str = depends_scheme
):
    """Put OSCAL system security plan for pvp component."""
    # TBD
    return 'OK'


# ===== Validation: results =====


@app.post(
    '/assessment-results/system-security-plan-id/system-security-plan-id',
    tags=['Validation: results'],
    response_model=str,
    description='Add a assessment-results for pvp component.'
)
async def add_system_assessment_results(
    system_security_plan_id: str, assessment_results: UploadFile, token: str = depends_scheme
):
    """Add assessment results."""
    # TBD
    return 'OK'
