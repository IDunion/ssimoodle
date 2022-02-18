from server.server import Server
from database.entities.credential import Credential
from database.handler.credential_handler import CredentialHandler
from database.handler.agent_handler import AgentHandler

from flask import request

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
    credential.data = str(data["Data"])

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

    # ToDo: Issue

    return str(True)

# Revoke a credential
@Server.app.route('/credential/revoke', methods=['Post'])
@Server.token_required
def revoke_credential():
    id = request.args["credentialId"]
    agentId = request.args["agentId"]

    credential = CredentialHandler.get(id)
    agent = AgentHandler.get(agentId)

    # ToDo: Revoke

    return str(True)