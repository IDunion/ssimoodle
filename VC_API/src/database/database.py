from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.setup import Setup
from global_settings import Settings

from database.entities.agent import Agent
from database.entities.credential import Credential
from database.entities.credential_issuing_data import CredentialIssuingData 

class Database:
    def run():
        sqlalchemy_engine = create_engine('sqlite:///' + Settings.databasePath + '/sqlalchemy.db?check_same_thread=False')
        Setup.Base.metadata.create_all(sqlalchemy_engine)
        Setup.Base.metadata.bind = sqlalchemy_engine

        DBSession = sessionmaker(bind=sqlalchemy_engine)
        Setup.SQL_Session = DBSession()