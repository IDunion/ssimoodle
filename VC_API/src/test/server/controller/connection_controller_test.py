import os, sys;
from pathlib import Path
from unittest import mock
path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import json
import unittest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import responses

from global_settings import Settings
from server.server import Server
from database.setup import Setup

# import controller
import server.controller.connection_controller

from database.entities.agent import Agent

class ConnectionControllerTest(unittest.TestCase):
    #### test route connection/connect #####
    @responses.activate
    def test_connect_returns_true(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Agent(id=1, name="Test1", api_token="Token", url="http://test.com"))

        responses.add(responses.POST, 'http://test.com/Connect',
                  json={"Test": "Test"}, status=200)

        res = Server.app.test_client().post(
            '/connection/connect?agentId=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data, b'test', "Expected True!")
        
if __name__ == '__main__':
    unittest.main()