from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.setup import Setup
from database.entities.credential_issuing_data import CredentialIssuingData

# Credential class
class Credential(Setup.Base):
    __tablename__ = 'Credential'
    
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, nullable=False)
    
    lms_user_id = Column(String(128), nullable=False)
    lms_course_id = Column(String(128), nullable=False)
    lms_issuer_id = Column(String(128), nullable=False)

    data = Column(String(1024), nullable=True)

    credential_data = relationship(CredentialIssuingData.__tablename__)