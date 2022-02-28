import os, sys;
from pathlib import Path
path = Path(os.path.realpath(__file__))
src = path.parent.parent.parent.absolute()
sys.path.append(os.path.dirname(src))
sys.path.append(os.path.join(os.path.dirname(src), "src"))

import unittest
from datetime import datetime

from server.server import Server
from database.entities.agent import Agent
from database.entities.credential import Credential

class ServerTest(unittest.TestCase):

    ##### test methode to_json_str #####
    def test_to_json_str_agent(self):
        date = datetime.now() 
        agent = Agent()
        agent.id = "1"
        agent.creation_date = date
        agent.name="Test"
        agent.url="test"
        agent.api_token="Secret"
        agent.vc_type="VC"

        expection = f'{{"id": "1", "creation_date": "{date.isoformat()}", "name": "Test", "url": "test", "api_token": "Secret", "vc_type": "VC"}}'
        res = Server.to_json_str(agent)
        self.assertEqual(res, expection, "Another json was expected!")

    def test_to_json_str_credential(self):
        date = datetime.now() 
        credential = Credential()
        credential.id = "1"
        credential.creation_date = date
        credential.user_id="Test"
        credential.course_id="test"
        credential.issuer_id="Issuer"
        credential.data='{"Data":"Test"}'

        expection = f'{{"id": "1", "creation_date": "{date.isoformat()}", "user_id": "Test", "course_id": "test", "issuer_id": "Issuer", "data": "{{\\"Data\\":\\"Test\\"}}"}}'
        res = Server.to_json_str(credential)
        self.assertEqual(res, expection, "Another json was expected!")

    ##### test wrapper token_required #####
    def test_token_required_no_token(self):
        with Server.app.test_request_context('url', headers={}):           
            def mock_func():
                return "Test"
            
            f = Server.token_required(mock_func)
            res = f()
            self.assertEqual(res[1], 401, "401 expected!")

    def test_token_required_wrong_token(self):
        with Server.app.test_request_context('url', headers={'x-auth-token': 'Test'}):           
            def mock_func():
                return "Test"
            
            f = Server.token_required(mock_func)
            res = f()
            self.assertEqual(res[1], 401, "401 expected!")

    def test_token_required_correct_token(self):
        with Server.app.test_request_context('url', headers={'x-auth-token': 'SecretToken'}):           
            def mock_func():
                return "Test"
            
            f = Server.token_required(mock_func)
            res = f()
            self.assertEqual(res, "Test", "'Test' expected!")
    
    ##### test wrapper contentType_json #####
    def test_contentType_json_wrong_typ(self):
        with Server.app.test_request_context('url', headers={'Content-Type': 'text'}):           
            def mock_func():
                return "Test"
            
            f = Server.contentType_json(mock_func)
            res = f()
            self.assertEqual(res[1], 415, "415 expected!")

    def test_contentType_json_correct_typ(self):
        with Server.app.test_request_context('url', headers={'Content-Type': 'application/json'}):           
            def mock_func():
                return "Test"
            
            f = Server.contentType_json(mock_func)
            res = f()
            self.assertEqual(res, "Test", "'Test' expected!")

    ##### test wrapper returns_json #####
    def test_returns_json_null(self):
        with Server.app.test_request_context('url', headers={}):           
            def mock_func():
                return None
            
            f = Server.returns_json(mock_func)
            res = f()
            self.assertEqual(res.status_code, 200, "Status code 200 expected!")
            self.assertEqual(res.data, b'{}', "{} expected!")

    def test_returns_json_obj(self):
        with Server.app.test_request_context('url', headers={}):
            date = datetime.now() 
            def mock_func():    
                agent = Agent()
                agent.id = "1"
                agent.creation_date = date
                agent.name="Test"
                agent.url="test"
                agent.api_token="Secret"
                agent.vc_type="VC"
                
                return agent
            
            f = Server.returns_json(mock_func)
            res = f()
            self.assertEqual(res.status_code, 200, "Status code 200 expected!")
            self.assertEqual(res.data, bytes(f'{{"id": "1", "creation_date": "{date.isoformat()}", "name": "Test", "url": "test", "api_token": "Secret", "vc_type": "VC"}}', encoding="utf-8"), "{} expected!")

    def test_returns_json_list(self):
        with Server.app.test_request_context('url', headers={}):
            date = datetime.now() 
            def mock_func():                
                agent = Agent()
                agent.id = "1"
                agent.creation_date = date
                agent.name="Test"
                agent.url="test"
                agent.api_token="Secret"
                agent.vc_type="VC"
                
                agent2 = Agent()
                agent2.id = "2"
                agent2.creation_date = date
                agent2.name="Test2"
                agent2.url="test2"
                agent2.api_token="Secret2"
                agent2.vc_type="VC2"

                return [agent, agent2]
            
            f = Server.returns_json(mock_func)
            res = f()
            self.assertEqual(res.status_code, 200, "Status code 200 expected!")
            self.assertEqual(res.data, bytes(f'[{{"id": "1", "creation_date": "{date.isoformat()}", "name": "Test", "url": "test", "api_token": "Secret", "vc_type": "VC"}}, {{"id": "2", "creation_date": "{date.isoformat()}", "name": "Test2", "url": "test2", "api_token": "Secret2", "vc_type": "VC2"}}]', encoding="utf-8"), "{} expected!")

if __name__ == '__main__':
    unittest.main()