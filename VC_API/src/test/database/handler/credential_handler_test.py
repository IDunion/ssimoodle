import os, sys;
from pathlib import Path

path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from database.setup import Setup
from database.entities.credential import Credential
from database.handler.credential_handler import CredentialHandler


class CredentialHandlerTest(unittest.TestCase):

    ##### test methode add #####
    def test_add_credential(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        credential = Credential(id=1)
        res = CredentialHandler.add(credential)

        self.assertEqual(res, 1, "Expected 1!")
        self.assertNotEqual(credential.creation_date, None, "Expected not null")

    ##### test methode get #####
    def test_get_return_credential(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1))
        
        res = CredentialHandler.get(1)

        self.assertEqual(res.id, 1, "Expected 1!")

    ##### test methode getlist #####
    def test_getAll_return_list(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1, course_id=1))
        Setup.SQL_Session.add(Credential(id=2, course_id=1))
        Setup.SQL_Session.add(Credential(id=3, course_id=1))
        
        query = {}
        res = CredentialHandler.getlist(query)

        self.assertEqual(len(res), 3, "Expected 3!")

if __name__ == '__main__':
    unittest.main()