from server.server import Server
from database.entities.agent import Agent
from database.handler.agent_handler import AgentHandler

from flask import request

# Gets an agent by id
@Server.app.route('/agent/get', methods=['Get'])
@Server.token_required
@Server.returns_json
def get_agent():
    """Returns an agent by id.
    ---
    tags:
      - Agents
    parameters:
      - name: id
        in: query 
        type: integer
        required: true
        default: 1
    definitions:
      Agent:
        type: object
        properties:
          id: 
            type: integer
          creationDate:
            type: string
          name:
            type: string
          url: 
            type: string
          api_token:
            type: string
          vc_type: 
            type: string
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The agent
        schema:
          $ref: '#/definitions/Agent'
    """
    id = request.args["id"]
    agent = AgentHandler.get(id)
    return agent

# Gets all agents
@Server.app.route('/agent/getall', methods=['Get'])
@Server.token_required
@Server.returns_json
def getAll_agent():
    """Returns all stored agents.
    ---
    tags:
      - Agents
    definitions:
      AgentList:
        type: array
        items:
          $ref: '#/definitions/Agent'
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The agent list
        schema:
          $ref: '#/definitions/AgentList'
    """
    agents = AgentHandler.getAll()
    return agents

# Stores a new agent
@Server.app.route('/agent/add', methods=['Post'])
@Server.token_required
def add_agent():
    """Stores a new agent.
    ---
    tags:
      - Agents
    parameters:
      - name: name
        in: query 
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: agent
          required:
            - url
            - token
            - type
          properties:
            url:
              type: string
              description: Agents url.
              default: localhost:123
            token:
              type: string
              description: Agents api token.
              default: SecretToken
            type:
              type: string
              description: Agents vc type.
              default: VC 2.0
    security:
      - APIKeyHeader: ['x-auth-token']
    responses:
      200:
        description: The id of the new agent.
        schema:
          ID: 
            type: integer
    """
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 415

    # id = request.args["id"]
    name = request.args["name"]
    data = request.json

    agent = Agent()
    agent.name = name
    agent.url = data["url"]
    agent.api_token = data["token"]
    agent.vc_type = data["type"]

    id = AgentHandler.add(agent)

    return str(id)