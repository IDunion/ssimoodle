import logging
import requests as http_client
from flask import request
from global_settings import Settings

from server.server import Server
from database.handler.agent_handler import AgentHandler

# Create new connection
@Server.app.route('/connection/connect', methods=['Post'])
@Server.token_required
def get_connection():
    """Creates an new connection by agent
    ---
    tags:
      - Connections
    parameters:
      - name: agentId
        in: query 
        type: integer
        required: true
        default: 1
      - name: body
        in: body
        required: true
        schema:
          id: userdata
          required:
            - userID
            - firstname
            - lastname
            - email
          properties:
            userId:
              type: string
              description: User id from the lms.
              default: 1
            firstname:
              type: string
              description: Firstname.
              default: Max
            lastname:
              type: string
              description: Lastname.
              default: Mustermann
            email:
              type: string
              description: Email.
              default: m@test.com      
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: True if successful, otherwise error (500).
        schema:
          Response: 
            bool: string
    """
    agent_id = request.args["agentId"]
    agent = AgentHandler.get(agent_id)
    
    data = request.json

    # Issuing
    url = agent.url + "/Connect"
    headers = {
        'x-auth-token': agent.api_token
        }
    body = data

    try:
        response = http_client.request("POST", url, headers=headers, json=body, verify=Settings.agentVerifySSL)
        if response.status_code == 200:
            return str(response.text)
        else:
            return f"Error. Agent provider returns {response.status_code}!", 500
    except http_client.exceptions.ConnectionError as ex:
        logging.error(ex)
        return "Can't connect to agent!", 500
    except Exception as ex:
        logging.error(ex)
        return "Unexpected exception!", 500