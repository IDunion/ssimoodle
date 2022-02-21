from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.setup import Setup

# Agent class
class Agent(Setup.Base):
    __tablename__ = 'Agent'
    
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, nullable=False)
    name = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    api_token = Column(String(256), nullable=False)
    vc_type = Column(String(32), nullable=True)

    credential_data = relationship("CredentialIssuingData")