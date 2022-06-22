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
import sqlite3 as db

from fastapi import HTTPException

from helper import helper

logger = logging.getLogger(__name__)


class Db():
    """Db."""

    def __init__(self, logger):
        """Init."""
        self.logger = logger
        self.con = db.connect('oscal.sqlite')
        self._init_catalog()
        self._init_profile()
        self._init_component_definition()
        self._init_system_security_plan()
        self._init_assessment_plan()
        self._init_assessment_results()
        self._init_plan_of_action_and_milestones()

    # TABLES

    def _init_table(self, tname, qcol=None):
        """Init table."""
        con = self.con
        with con:
            cur = con.cursor()
            query = f'SELECT name FROM sqlite_master WHERE type="table" AND name="{tname}";'  # noqa: S608
            list_tables = cur.execute(query).fetchall()
            if list_tables != []:
                con.commit()
                return
            if qcol is None:
                query = f'CREATE TABLE IF NOT EXISTS {tname} (id TEXT NOT NULL PRIMARY KEY, payload BLOB);'  # noqa: S608
            else:
                query = f'CREATE TABLE IF NOT EXISTS {tname} (id TEXT NOT NULL PRIMARY KEY, payload BLOB, {qcol} TEXT);'  # noqa: S608
            con.execute(query)

    def _key_exists_table(
        self,
        tname,
        oid,
    ):
        result = False
        con = self.con
        cur = con.cursor()
        query = f'SELECT * FROM {tname} WHERE id=?;'  # noqa: S608
        cur.execute(query, [oid])
        rows = cur.fetchall()
        if len(rows) == 1:
            result = True
        return result

    def _add_table(self, tname, oid, payload, cname=None, cvalue=None):
        """Add table."""
        try:
            con = self.con
            cur = con.cursor()
            if cname is None:
                query = f'INSERT INTO {tname} (id, payload) VALUES (?, ?);'  # noqa: S608
                cur.execute(query, [oid, payload])
            else:
                query = f'INSERT INTO {tname} (id, payload, {cname}) VALUES (?, ?, ?);'  # noqa: S608
                cur.execute(query, [oid, payload, cvalue])
            con.commit()
            result = oid
        except Exception:
            raise HTTPException(status_code=400, detail=f'{oid} already exists')
        return result

    def _replace_table(self, tname, oid, payload):
        """Replace table."""
        result = None
        try:
            if self._key_exists_table(tname, oid):
                con = self.con
                cur = con.cursor()
                query = f'REPLACE INTO {tname} (id, payload) VALUES (?, ?);'  # noqa: S608
                cur.execute(query, [oid, payload])
                con.commit()
                result = oid
        except Exception:
            raise HTTPException(status_code=400, detail=f'{oid} unable to replace')
        return result

    def _delete_table(self, tname, oid):
        """Delete table."""
        result = None
        try:
            if self._key_exists_table(tname, oid):
                con = self.con
                cur = con.cursor()
                query = f'DELETE FROM {tname} WHERE id=?;'  # noqa: S608
                cur.execute(query, [oid])
                con.commit()
                result = oid
        except Exception:
            raise HTTPException(status_code=400, detail=f'{oid} unable to delete')
        return result

    def _get_table(self, tname, oid):
        """Get table."""
        result = None
        try:
            con = self.con
            cur = con.cursor()
            query = f'SELECT * FROM {tname} WHERE id=?;'  # noqa: S608
            cur.execute(query, [oid])
            rows = cur.fetchall()
            if len(rows) == 1:
                result = rows[0][1]
        except Exception:
            raise HTTPException(status_code=400, detail=f'{oid} unable to get')
        return result

    def _get_table_id_list(self, tname):
        """Get table ids."""
        result = []
        try:
            con = self.con
            cur = con.cursor()
            query = f'SELECT * FROM {tname};'  # noqa: S608
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                result.append(row[0])
        except Exception:
            raise HTTPException(status_code=400, detail='unable to produce list')
        return result

    def _get_table_id_list_str(self, tname):
        """Get table ids as string."""
        return str(self._get_table_id_list(tname))

    def _get_table_by_column(self, tname, cname, cvalue):
        """Get table."""
        result = []
        try:
            con = self.con
            cur = con.cursor()
            query = f'SELECT * FROM {tname} WHERE {cname}=?;'  # noqa: S608
            cur.execute(query, [cvalue])
            rows = cur.fetchall()
            for row in rows:
                result.append(row[1])
        except Exception:
            raise HTTPException(status_code=400, detail=f'{tname} unable to get {cname} == {cvalue}')
        return result

    # CATALOGS

    def _init_catalog(self):
        """Init catalog."""
        self._init_table('CATALOGS')

    def add_catalog(self, oid, payload):
        """Add catalog."""
        return self._add_table('CATALOGS', oid, payload)

    def replace_catalog(self, oid, payload):
        """Replace catalog."""
        return self._replace_table('CATALOGS', oid, payload)

    def get_catalog(self, oid):
        """Get catalog."""
        return self._get_table('CATALOGS', oid)

    def delete_catalog(self, oid):
        """Delete catalog."""
        return self._delete_table('CATALOGS', oid)

    def get_catalog_id_list(self):
        """Get catalog ids."""
        return self._get_table_id_list_str('CATALOGS')

    # PROFILES

    def _init_profile(self):
        """Init profile."""
        self._init_table('PROFILES', helper.get_profile_mnemonic())

    def add_profile(self, oid, payload, profile_mnemonic):
        """Add profile."""
        return self._add_table('PROFILES', oid, payload, cname=helper.get_profile_mnemonic(), cvalue=profile_mnemonic)

    def replace_profile(self, oid, payload):
        """Replace profile."""
        return self._replace_table('PROFILES', oid, payload)

    def get_profile(self, oid):
        """Get profile."""
        return self._get_table('PROFILES', oid)

    def delete_profile(self, oid):
        """Delete profile."""
        return self._delete_table('PROFILES', oid)

    def get_profile_id_list(self):
        """Get profile ids."""
        return self._get_table_id_list_str('PROFILES')

    # COMPONENT DEFINITIONS

    def _init_component_definition(self):
        """Init component_definition."""
        self._init_table('COMPONENT_DEFINITIONS')

    def add_component_definition(self, oid, payload):
        """Add component_definition."""
        return self._add_table('COMPONENT_DEFINITIONS', oid, payload)

    def replace_component_definition(self, oid, payload):
        """Replace component_definition."""
        return self._replace_table('COMPONENT_DEFINITIONS', oid, payload)

    def get_component_definition(self, oid):
        """Get component_definition."""
        return self._get_table('COMPONENT_DEFINITIONS', oid)

    def delete_component_definition(self, oid):
        """Delete component_definition."""
        return self._delete_table('COMPONENT_DEFINITIONS', oid)

    def get_component_definition_id_list(self):
        """Get component_definition ids."""
        return self._get_table_id_list_str('COMPONENT_DEFINITIONS')

    # SYSTEM SECURITY PLANS

    def _init_system_security_plan(self):
        """Init system_security_plan."""
        self._init_table('SYSTEM_SECURITY_PLANS')

    def add_system_security_plan(self, oid, payload):
        """Add system_security_plan."""
        return self._add_table('SYSTEM_SECURITY_PLANS', oid, payload)

    def replace_system_security_plan(self, oid, payload):
        """Replace system_security_plan."""
        return self._replace_table('SYSTEM_SECURITY_PLANS', oid, payload)

    def get_system_security_plan(self, oid):
        """Get system_security_plan."""
        return self._get_table('SYSTEM_SECURITY_PLANS', oid)

    def delete_system_security_plan(self, oid):
        """Delete system_security_plan."""
        return self._delete_table('SYSTEM_SECURITY_PLANS', oid)

    def get_system_security_plan_id_list(self):
        """Get system_security_plan ids."""
        return self._get_table_id_list_str('SYSTEM_SECURITY_PLANS')

    # ASSESSMENT PLAN

    def _init_assessment_plan(self):
        """Init assessment_plan."""
        self._init_table('ASSESSMENT_PLANS')

    def add_assessment_plan(self, oid, payload):
        """Add assessment_plan."""
        return self._add_table('ASSESSMENT_PLANS', oid, payload)

    def replace_assessment_plan(self, oid, payload):
        """Replace assessment_plan."""
        return self._replace_table('ASSESSMENT_PLANS', oid, payload)

    def get_assessment_plan(self, oid):
        """Get assessment_plan."""
        return self._get_table('ASSESSMENT_PLANS', oid)

    def delete_assessment_plan(self, oid):
        """Delete assessment_plan."""
        return self._delete_table('ASSESSMENT_PLANS', oid)

    def get_assessment_plan_id_list(self):
        """Get assessment_plan ids."""
        return self._get_table_id_list_str('ASSESSMENT_PLANS')

    # ASSESSMENT RESULTS

    def _init_assessment_results(self):
        """Init assessment_results."""
        self._init_table('ASSESSMENT_RESULTS')

    def add_assessment_results(self, oid, payload):
        """Add assessment_results."""
        return self._add_table('ASSESSMENT_RESULTS', oid, payload)

    def replace_assessment_results(self, oid, payload):
        """Replace assessment_results."""
        return self._replace_table('ASSESSMENT_RESULTS', oid, payload)

    def get_assessment_results(self, oid):
        """Get assessment_results."""
        return self._get_table('ASSESSMENT_RESULTS', oid)

    def delete_assessment_results(self, oid):
        """Delete assessment_results."""
        return self._delete_table('ASSESSMENT_RESULTS', oid)

    def get_assessment_results_id_list(self):
        """Get assessment_results ids."""
        return self._get_table_id_list_str('ASSESSMENT_RESULTS')

    # PLAN OF ACTION AND MILESTONES

    def _init_plan_of_action_and_milestones(self):
        """Init plan_of_action_and_milestones."""
        self._init_table('PLAN_OF_ACTION_AND_MILESTONES')

    def add_plan_of_action_and_milestones(self, oid, payload):
        """Add plan_of_action_and_milestones."""
        return self._add_table('PLAN_OF_ACTION_AND_MILESTONES', oid, payload)

    def replace_plan_of_action_and_milestones(self, oid, payload):
        """Replace plan_of_action_and_milestones."""
        return self._replace_table('PLAN_OF_ACTION_AND_MILESTONES', oid, payload)

    def get_plan_of_action_and_milestones(self, oid):
        """Get plan_of_action_and_milestones."""
        return self._get_table('PLAN_OF_ACTION_AND_MILESTONES', oid)

    def delete_plan_of_action_and_milestones(self, oid):
        """Delete plan_of_action_and_milestones."""
        return self._delete_table('PLAN_OF_ACTION_AND_MILESTONES', oid)

    def get_plan_of_action_and_milestones_id_list(self):
        """Get plan_of_action_and_milestones ids."""
        return self._get_table_id_list_str('PLAN_OF_ACTION_AND_MILESTONES')

    # SEARCH PROFILES

    def search_profiles(self, profile_mnemonic):
        """Search profiles."""
        table = 'PROFILES'
        cname = helper.get_profile_mnemonic()
        cvalue = profile_mnemonic
        result = self._get_table_by_column(table, cname, cvalue)
        return result
