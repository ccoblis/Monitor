import mock
import unittest
from db import utils


class DbUtilsTestCase(unittest.TestCase):
    @mock.patch.object(utils, 'SessionClass')
    def _test_get_tmp_session(self, mock_session_class,
                                value_exception = False):
        try:
            with utils.get_tmp_session() as mock_session:
                self.assertEqual(
                    mock_session_class.return_value, 
                    mock_session)
                mock_session.commit.assert_called_once_with()    
                mock_session.close.assert_called_once_with()
            if value_exception:
                raise Exception
        except Exception:
            pass
        
    def test_get_tmp_session(self):
        self._test_get_tmp_session()
        
    def test_get_tmp_session_exception(self):
        self._test_get_tmp_session(True)
