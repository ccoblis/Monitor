import mock
import unittest
from db import api


class DbApiTestCase(unittest.TestCase):    
    def test_add_data_invalid_data(self):
        self.assertRaises(Exception, api.add_data)

    def test_add_data_update_entry_with_generate_id(self):
        pass

    def test_add_data_update_entry(self):
        pass

    def test_add_data_new_entry_with_generate_id(self):
        pass

    def test_add_data_new_entry(self):
        pass

    @mock.patch('db.api.uuid4')
    def _test_add_data_update_entry(self, mock_uuid4,
                            id, data, session):
        pass

    @mock.patch('db.api.uuid4')
    def _test_add_data_new_entry(self, mock_uuid4, 
                        id, data, session):
        pass
