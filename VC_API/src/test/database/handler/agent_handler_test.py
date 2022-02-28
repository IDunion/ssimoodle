import os, sys;
from pathlib import Path

path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from database.setup import Setup
from database.entities.agent import Agent
from database.handler.agent_handler import AgentHandler


class AgentHandlerTest(unittest.TestCase):

    ##### test methode add #####
    def test_add_agent(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        agent = Agent(id=1, name="Test1")
        res = AgentHandler.add(agent)

        self.assertEqual(res, 1, "Expected 1!")
        self.assertNotEqual(agent.creation_date, None, "Expected not null")

    ##### test methode get #####
    def test_get_return_agent(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Agent(id=1, name="Test1"))
        
        res = AgentHandler.get(1)

        self.assertEqual(res.id, 1, "Expected 1!")

    ##### test methode getall #####
    def test_getAll_return_list(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Agent(id=1, name="Test1"))
        Setup.SQL_Session.add(Agent(id=2, name="Test2"))
        Setup.SQL_Session.add(Agent(id=3, name="Test3"))
        
        res = AgentHandler.getAll()

        self.assertEqual(len(res), 3, "Expected 3!")

if __name__ == '__main__':
    unittest.main()