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
import os
import pathlib
import subprocess

base_url = os.environ.get('URL')
if base_url is None:
    base_url = 'https://oxp-swagger.nsn35y94ms7.us-south.codeengine.appdomain.cloud'
base_dir = (pathlib.Path.cwd()).parent

dir_trestle = base_dir / 'trestle.workspace'

file_catalog = dir_trestle / 'catalogs' / 'sample' / 'catalog.json'
file_profile = dir_trestle / 'profiles' / 'sample' / 'profile.json'
file_component_definition = dir_trestle / 'component-definitions' / 'sample' / 'component-definition.json'
file_system_security_plan = dir_trestle / 'system-security-plans' / 'sample' / 'system-security-plan.json'

file_assessment_results = dir_trestle / 'assessment-results' / 'assessment-results.json'

authorize = ['--oauth2-bearer', 'token']

get = ['curl', '-X', 'GET']
post = ['curl', '-X', 'POST']
put = ['curl', '-X', 'PUT']
delete = ['curl', '-X', 'DELETE']

def process(cmd):
    cmdline = ' '.join(cmd)
    print(cmdline)
    data = subprocess.run(cmd, capture_output=True)
    result = data.stdout.decode('utf-8').replace('"', '')
    print(result)
    return result

def fixup(id_):
    rval = id_.replace('{','').replace('}','').replace('detail:', '').replace('already exists', '').strip()
    #print(f'fixup: {id_} -> {rval}')
    return rval
    
def catalogs():
    print('*** Catalogs ***')
    result = process(get+[f'{base_url}/catalogs/id-list'])
    print('')
    result = process(post+[f'{base_url}/catalogs', '-F', f'catalog=@{file_catalog};type=application/json']+authorize)
    id_ = fixup(result)
    print('')
    result = process(get+[f'{base_url}/catalogs/id-list'])
    print('')
    contents = process(get+[f'{base_url}/catalogs/catalog-id?catalog_id={id_}'])
    print('')
    process(put+[f'{base_url}/catalogs/catalog-id?catalog_id={id_}', '-F', f'catalog=@{file_catalog};type=application/json']+authorize)
    print('')
    process(delete+[f'{base_url}/catalogs/catalog-id?catalog_id={id_}']+authorize)
    print('')
    result = process(get+[f'{base_url}/catalogs/id-list'])
    print('')
    
def profiles():
    print('*** Profiles ***')
    result = process(get+[f'{base_url}/profiles/id-list'])
    print('')
    result = process(post+[f'{base_url}/profiles', '-F', f'profile=@{file_profile};type=application/json']+authorize)
    id_ = fixup(result)
    print('')
    result = process(get+[f'{base_url}/profiles/id-list'])
    print('')
    contents = process(get+[f'{base_url}/profiles/profile-id?profile_id={id_}'])
    print('')
    process(put+[f'{base_url}/profiles/profile-id?profile_id={id_}', '-F', f'profile=@{file_profile};type=application/json']+authorize)
    print('')
    process(delete+[f'{base_url}/profiles/profile-id?profile_id={id_}']+authorize)
    print('')
    result = process(get+[f'{base_url}/profiles/id-list'])
    print('')
    
def component_definitions():
    print('*** Component Definitions ***')
    result = process(get+[f'{base_url}/component-definitions/id-list'])
    print('')
    result = process(post+[f'{base_url}/component-definitions', '-F', f'component_definition=@{file_component_definition};type=application/json']+authorize)
    id_ = fixup(result)
    print('')
    result = process(get+[f'{base_url}/component-definitions/id-list'])
    print('')
    contents = process(get+[f'{base_url}/component-definitions/component-definition-id?component_definition_id={id_}'])
    print('')
    process(put+[f'{base_url}/component-definitions/component-definition-id?component_definition_id={id_}', '-F', f'component_definition=@{file_component_definition};type=application/json']+authorize)
    print('')
    process(delete+[f'{base_url}/component-definitions/component-definition-id?component_definition_id={id_}']+authorize)
    print('')
    result = process(get+[f'{base_url}/component-definitions/id-list'])
    print('')

def system_security_plans():
    print('*** System Security Plans ***')
    result = process(get+[f'{base_url}/system-security-plans/id-list'])
    print('')
    result = process(post+[f'{base_url}/system-security-plans', '-F', f'system_security_plan=@{file_system_security_plan};type=application/json']+authorize)
    id_ = fixup(result)
    print('')
    result = process(get+[f'{base_url}/system-security-plans/id-list'])
    print('')
    contents = process(get+[f'{base_url}/system-security-plans/system-security-plan-id?system_security_plan_id={id_}'])
    print('')
    process(put+[f'{base_url}/system-security-plans/system-security-plan-id?system_security_plan_id={id_}', '-F', f'system_security_plan=@{file_system_security_plan};type=application/json']+authorize)
    print('')
    process(delete+[f'{base_url}/system-security-plans/system-security-plan-id?system_security_plan_id={id_}']+authorize)
    print('')
    result = process(get+[f'{base_url}/system-security-plans/id-list'])
    print('')

def validation_profile():
    print('*** Validation: Profile ***')
    # setup
    # post
    # tear down
    print('TBD')
    print('')
    
def validation_assessment_results():
    print('*** Validation: Assessment Results ***')
    # setup
    result = process(get+[f'{base_url}/system-security-plans/id-list'])
    print('')
    result = process(post+[f'{base_url}/system-security-plans', '-F', f'system_security_plan=@{file_system_security_plan};type=application/json']+authorize)
    id_ssp = fixup(result)
    print('')
    result = process(post+[f'{base_url}/profiles', '-F', f'profile=@{file_profile};type=application/json']+authorize)
    id_profile = fixup(result)
    print('')
    # post
    id_ = id_ssp
    result = process(post+[f'{base_url}/assessment-results/system-security-plan-id?system_security_plan_id={id_ssp}', '-F', f'assessment_results=@{file_assessment_results};type=application/json']+authorize)
    # tear down
    id_ = id_ssp
    process(delete+[f'{base_url}/system-security-plans/system-security-plan-id?system_security_plan_id={id_ssp}']+authorize)
    print('')
    id_ = id_profile
    process(delete+[f'{base_url}/profiles/profile-id?profile_id={id_}']+authorize)
    print('')
    
def main():
    catalogs()
    profiles()
    component_definitions()
    system_security_plans()
    validation_profile()
    validation_assessment_results()

if __name__ == "__main__":
    main()
