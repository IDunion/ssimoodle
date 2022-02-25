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

from database.entities.credential import Credential
from database.entities.agent import Agent
from database.entities.credential_issuing_data import CredentialIssuingData


# import controller
import server.controller.credential_controller

from globalSettings import Settings
from server.server import Server
from database.setup import Setup

class CredentialControllerTest(unittest.TestCase):

    ##### test route credential/get #####
    def test_get_agent_returns_none(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().get(
            '/credential/get?id=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data.decode("utf-8"), '{}', "Expected  {}!")

    def test_get_agent_returns_agent(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1, lms_user_id="1"))

        res = Server.app.test_client().get(
            '/credential/get?id=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(json.loads(res.data.decode("utf-8"))["lms_user_id"], "1", "Expected  {}!")

    ##### test route agent/getbycourseid #####
    def test_getbycourseid_returns_credentialList(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock(data=[
            (
            [mock.call.query(Credential),
            mock.call.filter(Credential.lms_course_id == "1")],
            [Credential(id=1, lms_course_id="1"), Credential(id=2, lms_course_id="1")]
        )])        

        res = Server.app.test_client().get(
            '/credential/getbycourseid?courseid=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(len(json.loads(res.data.decode("utf-8"))), 2, "Expected 2 credentias!")

    #### test route agent/add #####
    def test_add_agent_returns_ok(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().post(
            '/credential/add',
            data=json.dumps(dict(CourseId= "1", IssuerId= "1", UserId= "1", Data=dict(Date="20220101 00:00:00", Grade=0))),
            content_type='application/json',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")

    def test_add_agent_missing_contenttype(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()

        res = Server.app.test_client().post(
            '/credential/add',
            data=json.dumps(dict(CourseId= "1", IssuerId= "1", UserId= "1", Data=dict(Date="20220101 00:00:00", Grade=0))),
            headers={'x-auth-token': 'SecretToken'}
        )

        self.assertEqual(res.status_code, 415, "Expected 405!")

    #### test route credential/issue #####
    def test_issue_returns_true(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1, lms_user_id="1", data='{"Test":"Test"}'))
        Setup.SQL_Session.add(Agent(id=1, name="Test1", api_token="Token", url="http://test.com"))

        responses.add(responses.POST, 'http://test.com/Issue',
                  json={'Test': 'Test'}, status=200)

        res = Server.app.test_client().post(
            '/credential/issue?credentialId=1&agentId=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data, b'True', "Expected True!")
        
        cid = Setup.SQL_Session.query(CredentialIssuingData).filter(CredentialIssuingData.id == 1).first()

        self.assertEqual(cid.credential_id, '1', "Expected 1!")
        self.assertEqual(cid.agent_id, '1', "Expected 1!")
        self.assertEqual(cid.state, 1, "Expected 1!")

    #### test route credential/issuingresponse #####
    def test_issuingresponse_returns_true(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1, lms_user_id="1", data='{"Test":"Test"}'))
        Setup.SQL_Session.add(Agent(id=1, name="Test1", api_token="Token", url="http://test.com"))
        Setup.SQL_Session.add(CredentialIssuingData(id=1, credential_id="1", agent_id="1", state=1, data='{"Test":"Test"}'))

        res = Server.app.test_client().post(
            '/credential/issuingresponse?credentialId=1&agentId=1',
            data=json.dumps(dict(Test= "Test")),
            content_type='application/json',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data, b'True', "Expected True!")
        
        cid = Setup.SQL_Session.query(CredentialIssuingData).filter(CredentialIssuingData.id == 1).first()

        self.assertEqual(cid.state, 2, "Expected state 2!")
        self.assertEqual(cid.data, '{"Test": "Test"}', "Expected '{\"Test\": \"Test\"}'!")

    #### test route credential/revoke #####
    def test_revoke_returns_true(self):
        Setup.SQL_Session = UnifiedAlchemyMagicMock()
        Setup.SQL_Session.add(Credential(id=1, lms_user_id="1", data='{"Test":"Test"}'))
        Setup.SQL_Session.add(Agent(id=1, name="Test1", api_token="Token", url="http://test.com"))
        Setup.SQL_Session.add(CredentialIssuingData(id=1, credential_id="1", agent_id="1", state=1, data='{"Test":"Test"}'))

        responses.add(responses.POST, 'http://test.com/Revoke',
                  json={}, status=200)

        res = Server.app.test_client().post(
            '/credential/revoke?credentialId=1&agentId=1',
            headers={'x-auth-token': Settings.authToken}
        )

        self.assertEqual(res.status_code, 200, "Expected 200!")
        self.assertEqual(res.data, b'True', "Expected True!")
        
        cid = Setup.SQL_Session.query(CredentialIssuingData).filter(CredentialIssuingData.id == 1).first()

        self.assertEqual(cid.state, 3, "Expected 1!")

if __name__ == '__main__':
    unittest.main()