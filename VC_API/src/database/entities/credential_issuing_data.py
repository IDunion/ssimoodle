from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.setup import Setup
from enum import Enum

# Credential class
class CredentialIssuingData(Setup.Base):
    __tablename__ = 'CredentialIssuingData'
    
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    credential_id = Column(Integer, ForeignKey('Credential.id'))

    data = Column(String(1024), nullable=True)

# state enum
class State(Enum):
    Issuing = 1
    Issued = 2
    Revoked = 3