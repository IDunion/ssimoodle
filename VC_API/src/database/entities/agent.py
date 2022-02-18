from sqlalchemy import Column, Integer, String, DateTime
from database.setup import Setup

# Agent class
class Agent(Setup.Base):
    __tablename__ = 'Agent'
    
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, nullable=False)
    name = Column(String(250), nullable=False)
    configJson = Column(String(1024), nullable=False)