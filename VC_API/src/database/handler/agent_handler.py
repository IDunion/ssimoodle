from datetime import datetime 
from database.entities.agent import Agent
from database.setup import Setup

class AgentHandler():
    def add(agent) -> int:
        """Creates and stores a new agent

        Args:
            agent (Database.Entities.Agent): The agent which will be stored

        Returns:
            id: The id of the agent
        """
        agent.creation_date = datetime.now()

        Setup.SQL_Session.add(agent)
        Setup.SQL_Session.commit()
        return agent.id
    
    def update():
        Setup.SQL_Session.commit()

    def get(id) -> Agent:
        """Gets an agent by id

        Args:
            id (int): agent id

        Returns:
            Database.Entities.Agent: The agent
        """
        return Setup.SQL_Session.query(Agent).filter(Agent.id == id).first()

    def getAll() -> list:
        """Gets all agents

        Returns:
            List(Database.Entities.Agent): List of agents
        """
        return Setup.SQL_Session.query(Agent).all()