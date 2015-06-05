import mock
import unittest
from agents import api


class AgentsTestCase(unittest.TestCase):
    @mock.patch('agents.api.platform.system')
    def test_agent_platform_unsupported_os(self, mock_system):
        mock_system.return_value = "MacOS"
        self.assertRaises(Exception, api.Agents)

    @mock.patch('agents.api.platform.system')
    def test_agent_platform_supported_os(self, mock_system):
        mock_system.return_value = "Windows"
        try:
            a = api.Agents()
        except Exception:
            self.fail("api.Agents() raises Exception unexpectedly!")
