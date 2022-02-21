import json
import logging
import requests as http_client
from flask import request

from server.server import Server
from database.entities.credential import Credential, State
from database.entities.credential_issuing_data import CredentialIssuingData

from database.handler.credential_handler import CredentialHandler
from database.handler.agent_handler import AgentHandler
from database.handler.credential_issuing_data_handler import CredentialIssuingDataHandler

# Gets a credential by id
@Server.app.route('/credential/get', methods=['Get'])
@Server.token_required
@Server.returns_json
def get_credential():
    id = request.args["id"]
    credential = CredentialHandler.get(id)
    return credential

# Gets all credentials by course id
@Server.app.route('/credential/getbycourseid', methods=['Get'])
@Server.token_required
@Server.returns_json
def getByCourseId_credential():
    courseId = request.args["courseid"]
    credentials = CredentialHandler.getByCourseId(courseId)
    return credentials

# Stores a new credential
@Server.app.route('/credential/add', methods=['Post'])
@Server.token_required
@Server.contentType_json
def add_credential():
    data = request.json

    credential = Credential()
    credential.lms_user_id = data["UserId"]
    credential.lms_course_id = data["CourseId"]
    credential.lms_issuer_id = data["IssuerId"]
    credential.data = json.dumps(data["Data"])

    id = CredentialHandler.add(credential)

    return str(id)

# Issue a credential
@Server.app.route('/credential/issue', methods=['Post'])
@Server.token_required
def issue_credential():
    id = request.args["credentialId"]
    agentId = request.args["agentId"]

    credential = CredentialHandler.get(id)
    agent = AgentHandler.get(agentId)

    # Issuing
    url = agent.url + "/Issuing"
    headers = {
        'x-auth-token': agent.api_token
        }
    body = json.loads(credential.data)

    try:
        response = http_client.request("POST", url, headers=headers, data=body)
        if response.status_code == 200:
            credential.state = State.Issuing.value
            CredentialHandler.update()

            return str(True)
        else:
            return f"Error. Agent provider returns {response.status_code}!", 500
    except http_client.exceptions.ConnectionError as ex:
        logging.error(ex)
        return "Can't connect to agent!", 500
    except Exception as ex:
        logging.error(ex)
        return "Unexpected exception!", 500

# The issuing response from the agent
@Server.app.route('/credential/issuingresponse', methods=['Post'])
@Server.token_required
@Server.contentType_json
def issuingresponse_credential():
    id = request.args["credentialId"]
    agentId = request.args["agentId"]
    
    data = request.json

    credential = CredentialHandler.get(id)
    credential.state = State.Issued.value

    credentialIssiungData = CredentialIssuingData()
    credentialIssiungData.credential_id = id
    credentialIssiungData.agent_id = agentId
    credentialIssiungData.data = json.dumps(data)
    CredentialIssuingDataHandler.add(credentialIssiungData)

    return str(True)
    
# Revoke a credential
@Server.app.route('/credential/revoke', methods=['Post'])
@Server.token_required
def revoke_credential():
    credentialId = request.args["credentialId"]
    agentId = request.args["agentId"]

    credential = CredentialHandler.get(credentialId)
    agent = AgentHandler.get(agentId)
    credentialIssuingData = CredentialIssuingDataHandler.getByCredentialAndAgent(credentialId, agentId)

    # Revoke
    url = agent.url + "/Revoke"
    headers = {
        'x-auth-token': agent.api_token
        }
    body = json.loads(credentialIssuingData.data)

    try:
        response = http_client.request("POST", url, headers=headers, data=body)
        if response.status_code == 200:
            credential.state = State.Revoked.value
            CredentialHandler.update()

            return str(True)
        else:
            return f"Error. Agent provider returns {response.status_code}!", 500
    except http_client.exceptions.ConnectionError as ex:
        logging.error(ex)
        return "Can't connect to agent!", 500
    except Exception as ex:
        logging.error(ex)
        return "Unexpected exception!", 500