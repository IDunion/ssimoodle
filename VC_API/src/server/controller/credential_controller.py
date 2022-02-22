import json
import logging
import requests as http_client
from flask import request

from server.server import Server
from database.entities.credential import Credential
from database.entities.credential_issuing_data import CredentialIssuingData, State

from database.handler.credential_handler import CredentialHandler
from database.handler.agent_handler import AgentHandler
from database.handler.credential_issuing_data_handler import CredentialIssuingDataHandler

# Gets a credential by id
@Server.app.route('/credential/get', methods=['Get'])
@Server.token_required
@Server.returns_json
def get_credential():
    """Returns a credential by id.
    ---
    tags:
      - Credentials
    parameters:
      - name: id
        in: query 
        type: integer
        required: true
        default: 1
    definitions:
      Credential:
        type: object
        properties:
          id: 
            type: integer
          creationDate:
            type: string
          lms_user_id:
            type: string
          lms_course_id: 
            type: string
          lms_issuer_id:
            type: string
          data: 
            type: string
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The credential
        schema:
          $ref: '#/definitions/Credential'
    """
    id = request.args["id"]
    credential = CredentialHandler.get(id)
    return credential

# Gets all credentials by course id
@Server.app.route('/credential/getbycourseid', methods=['Get'])
@Server.token_required
@Server.returns_json
def getByCourseId_credential():
    """Returns all stored credentials by course id.
    ---
    tags:
      - Credentials
    parameters:
      - name: courseid
        in: query 
        type: integer
        required: true
        default: 1
    definitions:
      CredentialList:
        type: array
        items:
          $ref: '#/definitions/Credential'
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The credential list
        schema:
          $ref: '#/definitions/CredentialList'
    """
    courseId = request.args["courseid"]
    credentials = CredentialHandler.getByCourseId(courseId)
    return credentials

# Stores a new credential
@Server.app.route('/credential/add', methods=['Post'])
@Server.token_required
@Server.contentType_json
def add_credential():
    """Stores a new credential.
    ---
    tags:
      - Credentials
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: credential
          required:
            - UserId
            - CourseId
            - IssuerId
            - Data
          properties:
            UserId:
              type: string
              description: User id from the lms.
              default: localhost:123
            CourseId:
              type: string
              description: Course id from the lms.
              default: SecretToken
            IssuerId:
              type: string
              description: Issuer id from the lms system.
              default: VC 2.0
            Data:
              type: object
              properties:
                Grade:
                  type: integer
                  description: The grade of the student.
                  default: 1
                Date:
                  type: string
                  description: The date of the course.
                  default: 2022-02-16
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The id of the new agent.
        schema:
          ID: 
            type: integer
    """
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
    """Starts the issuing process by calling the agent.
    ---
    tags:
      - Credentials
    parameters:
      - name: credentialId
        in: query 
        type: integer
        required: true
        default: 1
      - name: agentId
        in: query 
        type: integer
        required: true
        default: 1
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: True if successful, otherwise error (500).
        schema:
          Response: 
            bool: string
    """
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
            credentialIssiungData = CredentialIssuingData()
            credentialIssiungData.credential_id = id
            credentialIssiungData.agent_id = agentId
            credentialIssiungData.state = State.Issuing.value
            CredentialIssuingDataHandler.add(credentialIssiungData)

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
    """Response from the agent. Stores the issuing data.
    ---
    tags:
      - Credentials
    parameters:
      - name: credentialId
        in: query 
        type: integer
        required: true
        default: 1
      - name: agentId
        in: query 
        type: integer
        required: true
        default: 1
      - name: body
        in: body
        required: true
        schema:
          id: response
          required:
            - SomeValue
          properties:
            SomeValue:
              type: string
              description: Some issuing value.
              default: Some issiung value.
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: True if successful, otherwise error (500).
        schema:
          Response: 
            bool: string
    """
    id = request.args["credentialId"]
    agentId = request.args["agentId"]
    
    data = request.json

    credential = CredentialHandler.get(id)
    credential.state = State.Issued.value

    credentialIssiungData = CredentialIssuingDataHandler.getByCredentialAndAgent(id, agentId)
    credentialIssiungData.state = State.Issued.value
    credentialIssiungData.data = json.dumps(data)
    CredentialIssuingDataHandler.update()

    return str(True)

# Revoke a credential
@Server.app.route('/credential/revoke', methods=['Post'])
@Server.token_required
def revoke_credential():
    """Starts the revocation process by calling the agent.
    ---
    tags:
      - Credentials
    parameters:
      - name: credentialId
        in: query 
        type: integer
        required: true
        default: 1
      - name: agentId
        in: query 
        type: integer
        required: true
        default: 1
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: True if successful, otherwise error (500).
        schema:
          Response: 
            bool: string
    """
    credentialId = request.args["credentialId"]
    agentId = request.args["agentId"]

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
            credentialIssuingData.state = State.Revoked.value
            CredentialIssuingDataHandler.update()

            return str(True)
        else:
            return f"Error. Agent provider returns {response.status_code}!", 500
    except http_client.exceptions.ConnectionError as ex:
        logging.error(ex)
        return "Can't connect to agent!", 500
    except Exception as ex:
        logging.error(ex)
        return "Unexpected exception!", 500