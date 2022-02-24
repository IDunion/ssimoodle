import unittest
from test.server.server_test import ServerTest

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(ServerTest))

runner=unittest.TextTestRunner()
runner.run(test_suite)