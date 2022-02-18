from server.server import Server
from database.entities.agent import Agent
from database.handler.agent_handler import AgentHandler

from flask import request

# Gets an agent by id
@Server.app.route('/agent/get', methods=['Get'])
@Server.token_required
@Server.returns_json
def get_agent():
    id = request.args["id"]
    agent = AgentHandler.get(id)
    return agent

# Gets all agents
@Server.app.route('/agent/getall', methods=['Get'])
@Server.token_required
@Server.returns_json
def getAll_agent():
    agents = AgentHandler.getAll()
    return agents

# Stores a new agent
@Server.app.route('/agent/add', methods=['Post'])
@Server.token_required
def add_agent():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 415

    # id = request.args["id"]
    name = request.args["name"]
    data = request.json

    agent = Agent()
    agent.name = name
    agent.configJson = str(data)

    id = AgentHandler.add(agent)

    return str(id)