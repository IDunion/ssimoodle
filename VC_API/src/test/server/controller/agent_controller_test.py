import os, sys;
from pathlib import Path
path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import json
import unittest

from database.entities.agent import Agent
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

# import controller
import server.controller.agent_controller

from globalSettings import Settings
from server.server import Server
from database.setup import Setup

class AgentControllerTest(unittest.TestCase):

    ##### test route agent/get #####
    def test_get_agent_returns_none(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().get(
            '/agent/get?id=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data.decode("utf-8"), '{}', "Expected  {}!")

    def test_get_agent_returns_agent(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Agent(id=1, name="Test"))

        res = Server.app.test_client().get(
            '/agent/get?id=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(json.loads(res.data.decode("utf-8"))["name"], "Test", "Expected  {}!")

    ##### test route agent/getall #####
    def test_getAll_agent_returns_agentList(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Agent(id=1, name="Test1"))
        Setup.SQL_Session.add(Agent(id=2, name="Test2"))
        Setup.SQL_Session.add(Agent(id=3, name="Test3"))

        res = Server.app.test_client().get(
            '/agent/getall',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(len(json.loads(res.data.decode("utf-8"))), 3, "Expected json!")

    ##### test route agent/add #####
    def test_add_agent_returns_ok(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().post(
            '/agent/add?name=Test',
            data=json.dumps(dict(token="Test",type="vc",url="test.com")),
            content_type='application/json',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")

    def test_add_agent_missing_contenttype(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().post(
            '/agent/add?name=Test',
            data=json.dumps(dict(token="Test",type="vc",url="test.com")),
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 415, "Expected 405!")

if __name__ == '__main__':
    unittest.main()