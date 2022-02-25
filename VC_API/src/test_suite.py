import unittest
from test.server.server_test import ServerTest
from test.server.controller.agent_controller_test import AgentControllerTest
from test.server.controller.credential_controller_test import CredentialControllerTest
from test.database.handler.agent_handler_test import AgentHandlerTest
from test.database.handler.credential_handler_test import CredentialHandlerTest
from test.database.handler.credential_issuing_data_handler_test import CredentialIssuingdataHandlerTest


test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(ServerTest))
test_suite.addTest(unittest.makeSuite(AgentControllerTest))
test_suite.addTest(unittest.makeSuite(CredentialControllerTest))

test_suite.addTest(unittest.makeSuite(AgentHandlerTest))
test_suite.addTest(unittest.makeSuite(CredentialHandlerTest))
test_suite.addTest(unittest.makeSuite(CredentialIssuingdataHandlerTest))

runner=unittest.TextTestRunner()
runner.run(test_suite)