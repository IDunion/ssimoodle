from sqlalchemy import Column, Integer, String, DateTime
from database.setup import Setup
from enum import Enum

# Credential class
class Credential(Setup.Base):
    __tablename__ = 'Credential'
    
    id = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    
    lms_user_id = Column(String(128), nullable=False)
    lms_course_id = Column(String(128), nullable=False)
    lms_issuer_id = Column(String(128), nullable=False)

    data = Column(String(1024), nullable=True)

# state enum
class Status(Enum):
    Created = 1
    Issuing = 2
    Issued = 3
    Revoked = 4