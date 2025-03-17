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


# ----------
# Authentication
#----------


@app.post('/token', include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = depends):
    """Authenticate user."""
    token = str(uuid.uuid4())
    return {'access_token': token, 'token_type': 'bearer'}


# ----------
# Catalogs
# ----------


@app.post(
    '/catalogs', tags=['Lifecycle: Catalogs'], response_model=str, description='Add an OSCAL catalog in datastore.'
)
async def add_catalog(catalog: UploadFile, token: str = depends_scheme):
    """Add OSCAL catalog."""
    oscal_path = 'catalog'
    oscal_file = catalog
    logger.info('add catalog')
    try:
        # get a wrapped object
        element_path = elements.ElementPath(oscal_path)
        logger.info('element_path: {element_path}')
        obm_type = element_path.get_obm_wrapped_type()
        # get contents as string
        contents = str(await oscal_file.read(), 'utf-8')
        # save in temp file
        temp_path = pathlib.Path(tempfile.gettempdir()) / 'upload.json'
        
        logger.info('temp_path: {temp_path}')
        
        with open(temp_path, 'w') as f:
            f.write(contents)
        # validate
        oscal = obm_type.oscal_read(temp_path)
    except Exception:
        text = f'Invalid {oscal_path} in file.'
        logger.error(f'add catalog: {text}')
        raise HTTPException(status_code=400, detail=text)
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


    
    
    
    
    