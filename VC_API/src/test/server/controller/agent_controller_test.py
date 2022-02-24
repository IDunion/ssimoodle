import os, sys;
from pathlib import Path
path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from datetime import datetime

from database.entities.agent import Agent
from server.controller.agent_controller import get_agent
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from server.server import Server
from database.setup import Setup

class AgentControllerTest(unittest.TestCase):

    ##### test methode to_json_str #####
    def test_get_agent_returns_none(self):
        agent = Agent()
        agent.id = "1"
        agent.creationDate = datetime.now()
        agent.name="Test"
        agent.url="test"
        agent.api_token="Secret"
        agent.vc_type="VC"

        with Server.app.test_request_context() as req:
            req.request.args = {'id': '1'}             
            Setup.SQL_Session = UnifiedAlchemyMagicMock()
            func = get_agent.__wrapped__.__wrapped__
            res = func()
            self.assertEqual(res, None, "Expected None!")

    ##### test methode to_json_str #####
    def test_get_agent_returns_agent(self):
        agent = Agent()
        agent.id = "1"
        agent.creationDate = datetime.now()
        agent.name="Test"
        agent.url="test"
        agent.api_token="Secret"
        agent.vc_type="VC"

        with Server.app.test_request_context() as req:
            req.request.args = {'id': '1'}             

            Setup.SQL_Session = UnifiedAlchemyMagicMock()
            Setup.SQL_Session.add(Agent(id=1, name="Test"))

            func = get_agent.__wrapped__.__wrapped__
            res = func()
            self.assertEqual(res.name, "Test", "Expected None!")

if __name__ == '__main__':
    unittest.main()