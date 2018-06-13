# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Asket Agarwal, <asket.agarwal96@gmail.com>

from nose.tools import assert_equal, assert_is_instance, assert_in

from rucio.client.didclient import DIDClient
from rucio.common.utils import generate_uuid as uuid
from rucio.common.exception import RucioException


class TestDidMetaClient():

    def setup(self):
        self.did_client = DIDClient()
        self.tmp_scope = 'mock'
        self.tmp_name = 'name_%s' % uuid()
        self.did_client.add_did(scope=self.tmp_scope, name=self.tmp_name, type="DATASET")

    def test_add_did_meta(self):
        """ META (CLIENTS) : Adds a fully set json column to a did, updates if some keys present """
        try:
            data = {"key1": "value_" + str(uuid()), "key2": "value_" + str(uuid()), "key3": "value_" + str(uuid())}
            self.did_client.add_did_meta(scope=self.tmp_scope, name=self.tmp_name, meta=data)

            data = {"key4": "value_" + str(uuid()), "key5": "value_" + str(uuid())}
            self.did_client.add_did_meta(scope=self.tmp_scope, name=self.tmp_name, meta=data)

            metadata = self.did_client.get_did_meta(scope=self.tmp_scope, name=self.tmp_name)
            assert_equal(len(metadata), 5)

        except RucioException:
            pass

    def test_delete_generic_metadata(self):
        """ META (CLIENTS) : Deletes metadata key """
        try:
            data = {"key1": "value_" + str(uuid()), "key2": "value_" + str(uuid()), "key3": "value_" + str(uuid())}
            self.did_client.add_did_meta(scope=self.tmp_scope, name=self.tmp_name, meta=data)

            key = "key2"
            self.did_client.delete_did_meta(scope=self.tmp_scope, name=self.tmp_name, key=key)
            metadata = self.did_client.get_did_meta(scope=self.tmp_scope, name=self.tmp_name)
            assert_equal(len(metadata), 2)

        except RucioException:
            pass

    def test_get_generic_metadata(self):
        """ META (CLIENTS) : Gets all metadata for the given did """
        try:
            data = {"key1": "value_" + str(uuid()), "key2": "value_" + str(uuid()), "key3": "value_" + str(uuid())}
            self.did_client.add_did_meta(scope=self.tmp_scope, name=self.tmp_name, meta=data)

            metadata = self.did_client.get_did_meta(scope=self.tmp_scope, name=self.tmp_name)
            assert_equal(metadata, data)

        except RucioException:
            pass

    def test_list_dids_by_generic_meta(self):
        """ META (CLIENTS) : Get all dids matching the values of the provided metadata keys """
        try:
            tmp_scope = 'mock'

            for i in range(5):
                tmp_name = 'name_%s' % str(i)
                self.did_client.add_did(scope=tmp_scope, name=tmp_name, type="DATASET")
                data = {"key1": "value_" + str(uuid()), "key2": "value_" + str(uuid()), "key3": "value_" + str(uuid())}
                self.did_client.add_did_meta(scope=tmp_scope, name=tmp_name, meta=data)

            temp_val = self.did_client.get_did_meta(scope=tmp_scope, name="name_1")
            select_query = {"key1": temp_val["key1"], "key2": temp_val["key2"]}
            dids = self.did_client.list_dids_by_meta(scope=tmp_scope, select=select_query)
            assert_is_instance(dids, list)
            assert_equal(len(dids), 1)
            assert_in({'scope': 'mock', 'name': 'name_1'}, dids)

        except RucioException:
            pass
