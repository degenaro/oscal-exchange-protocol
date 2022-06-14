# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2022 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""OSCAL Exchange Protocol."""

import json
import logging

from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


class Helper():
    """Helper functions."""

    def __init__(self):
        """Initialize."""
        yaml = YAML(typ='safe')
        with open('./app.yaml', 'r') as f:
            self.config = yaml.load(f)

    def get_version(self):
        """Get version."""
        return self.config['app-version']

    def get_profile_mnemonic(self):
        """Get profile mnemonic."""
        return self.config['profile-mnemonic']

    def get_profile_phase_i(self):
        """Get profile phase i."""
        fp = self.config['profile-phase-i']
        with open(fp, 'r') as f:
            jdata = json.load(f)
            if 'profile' in jdata:
                profile = jdata['profile']
            else:
                profile = jdata
            return profile

    def get_ssp_phase_i(self):
        """Get ssp phase i."""
        fp = self.config['ssp-phase-i']
        with open(fp, 'r') as f:
            jdata = json.load(f)
            if 'system-security-plan' in jdata:
                ssp = jdata['system-security-plan']
            else:
                ssp = jdata
            return ssp

    def get_ssp_phase_ii(self):
        """Get ssp phase ii."""
        fp = self.config['ssp-phase-ii']
        with open(fp, 'r') as f:
            jdata = json.load(f)
            if 'system-security-plan' in jdata:
                ssp = jdata['system-security-plan']
            else:
                ssp = jdata
            return ssp


helper = Helper()
