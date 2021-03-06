import os
import datetime
import unittest
from decimal import Decimal

import requests_mock

from datapackage_pipelines.utilities.lib_test_helpers import (
    mock_processor_test
)

import datapackage_pipelines_spss.processors

import logging
log = logging.getLogger(__name__)

ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')


class TestAddSpssProcessor(unittest.TestCase):

    def test_add_spss_processor_from_path(self):

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'project': 'my-project',
            'resources': []
        }
        params = {
            'source': 'data/Employee data.sav'
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_spss.processors.__file__)
        processor_path = os.path.join(processor_dir, 'add_spss.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]
        spew_res_iter = spew_args[1]

        # Asserts for the datapackage
        dp_resources = spew_dp['resources']
        assert len(dp_resources) == 1
        assert dp_resources[0]['name'] == 'employee-data-sav'
        field_names = \
            [field['name'] for field in dp_resources[0]['schema']['fields']]
        assert field_names == [
            'id',
            'gender',
            'bdate',
            'educ',
            'jobcat',
            'salary',
            'salbegin',
            'jobtime',
            'prevexp',
            'minority'
        ]

        # Asserts for the res_iter
        spew_res_iter_contents = list(spew_res_iter)
        # One resourse
        assert len(spew_res_iter_contents) == 1
        rows = list(spew_res_iter_contents[0])
        assert len(rows) == 474
        assert rows[0] == \
            {'id': 1, 'gender': 'm', 'bdate': datetime.date(1952, 2, 3),
             'educ': 15, 'jobcat': 3, 'salary': Decimal('57000'),
             'salbegin': Decimal('27000'), 'jobtime': 98, 'prevexp': 144,
             'minority': 0}

    @requests_mock.mock()
    def test_add_spss_processor_from_url(self, mock_request):
        '''source is a url'''

        # mock the http response
        mock_data_file = open('data/Employee data.sav', mode='r+b')
        mock_response = mock_data_file.read()
        mock_data_file.close()
        mock_request.get('https://example.com/Employee%20data.sav',
                         content=mock_response)

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'project': 'my-project',
            'resources': []
        }
        params = {
            'source': 'https://example.com/Employee%20data.sav'
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_spss.processors.__file__)
        processor_path = os.path.join(processor_dir, 'add_spss.py')

        # Trigger the processor with our mock `ingest` and capture what it will
        # returned to `spew`.
        spew_args, _ = mock_processor_test(processor_path,
                                           (params, datapackage, []))

        spew_dp = spew_args[0]
        spew_res_iter = spew_args[1]

        # Asserts for the datapackage
        dp_resources = spew_dp['resources']
        assert len(dp_resources) == 1
        assert dp_resources[0]['name'] == 'employee-data-sav'
        field_names = \
            [field['name'] for field in dp_resources[0]['schema']['fields']]
        assert field_names == [
            'id',
            'gender',
            'bdate',
            'educ',
            'jobcat',
            'salary',
            'salbegin',
            'jobtime',
            'prevexp',
            'minority'
        ]

        # Asserts for the res_iter
        spew_res_iter_contents = list(spew_res_iter)
        # One resourse
        assert len(spew_res_iter_contents) == 1
        rows = list(spew_res_iter_contents[0])
        assert len(rows) == 474
        assert rows[0] == \
            {'id': 1, 'gender': 'm', 'bdate': datetime.date(1952, 2, 3),
             'educ': 15, 'jobcat': 3, 'salary': Decimal('57000'),
             'salbegin': Decimal('27000'), 'jobtime': 98, 'prevexp': 144,
             'minority': 0}

    def test_add_spss_processor_from_path_bad_format(self):
        '''source with bad format raises exception'''

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'project': 'my-project',
            'resources': []
        }
        params = {
            'source': 'data/Employee data.csv'
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_spss.processors.__file__)
        processor_path = os.path.join(processor_dir, 'add_spss.py')

        with self.assertRaises(RuntimeError):
            mock_processor_test(processor_path, (params, datapackage, []))

    def test_add_spss_processor_bad_scheme(self):
        '''source with unsupported scheme raises exception'''

        # input arguments used by our mock `ingest`
        datapackage = {
            'name': 'my-datapackage',
            'project': 'my-project',
            'resources': []
        }
        params = {
            'source': 'ftp://example.com/Employee data.sav'
        }

        # Path to the processor we want to test
        processor_dir = \
            os.path.dirname(datapackage_pipelines_spss.processors.__file__)
        processor_path = os.path.join(processor_dir, 'add_spss.py')

        with self.assertRaises(RuntimeError):
            mock_processor_test(processor_path, (params, datapackage, []))
