from datetime import datetime 
from database.entities.credential import Credential
from database.setup import Setup

class CredentialHandler():
    def add(credential) -> int:
        """Creates and stores a new credential

        Args:
            credential (Database.Entities.Credential): Credential which will be stored

        Returns:
            int: The id of the credential
        """
        credential.creation_date = datetime.now()

        Setup.SQL_Session.add(credential)
        Setup.SQL_Session.commit()
        return credential.id

    def update():
        Setup.SQL_Session.commit()
    
    def get(id) -> Credential:
        """Gets a credential by id
        
        Args:
            id (int): credential id

        Returns:
            Database.Entities.Credential: The credential
        """
        return Setup.SQL_Session.query(Credential).filter(Credential.id == id).first()

    def getlist(query) -> list:
        """Returns all credential by the given query parameters

        Args:
            query (Dict): The packed query dictonary

        Returns:
            List(Database.Entities.Credential): List of credentials
        """
        return Setup.SQL_Session.query(Credential).filter_by(**query).all()