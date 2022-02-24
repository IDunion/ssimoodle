import os, sys;
from pathlib import Path
path = Path(os.path.realpath(__file__))
src = path.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from test.server.server_test import ServerTest

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(ServerTest))

runner=unittest.TextTestRunner()
runner.run(test_suite)