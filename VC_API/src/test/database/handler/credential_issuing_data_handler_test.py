import os, sys;
from pathlib import Path

path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from database.setup import Setup
from database.entities.credential_issuing_data import CredentialIssuingData
from database.handler.credential_issuing_data_handler import CredentialIssuingDataHandler


class CredentialIssuingdataHandlerTest(unittest.TestCase):

    ##### test methode add #####
    def test_add_credentialissuingdata(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        cid = CredentialIssuingData(id=1)
        res = CredentialIssuingDataHandler.add(cid)

        self.assertEqual(res, 1, "Expected 1!")
        self.assertNotEqual(cid.creationDate, None, "Expected not null")

    ##### test methode get #####
    def test_get_return_credential(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(CredentialIssuingData(id=1))
        
        res = CredentialIssuingDataHandler.get(1)

        self.assertEqual(res.id, 1, "Expected 1!")

    ##### test methode getall #####
    def test_getAll_return_list(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(CredentialIssuingData(id=1, credential_id=1, agent_id=1))
        
        res = CredentialIssuingDataHandler.getByCredentialAndAgent(1, 1)

        self.assertEqual(res.credential_id, 1, "Expected 2!")

if __name__ == '__main__':
    unittest.main()