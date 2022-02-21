from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.setup import Setup

# Credential class
class CredentialIssuingData(Setup.Base):
    __tablename__ = 'CredentialIssuingData'
    
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, nullable=False)
    
    agent_id = Column(Integer, ForeignKey('Agent.id'))
    credential_id = Column(Integer, ForeignKey('Credential.id'))

    data = Column(String(1024), nullable=True)