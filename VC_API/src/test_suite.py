import unittest
from test.server.server_test import ServerTest
from test.server.controller.agent_controller_test import AgentControllerTest

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(ServerTest))
test_suite.addTest(unittest.makeSuite(AgentControllerTest))

runner=unittest.TextTestRunner()
runner.run(test_suite)