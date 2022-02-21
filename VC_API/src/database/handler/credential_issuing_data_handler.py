from datetime import datetime
from database.entities.credential_issuing_data import CredentialIssuingData
from database.setup import Setup

class CredentialIssuingDataHandler():
    def add(credentialIssiungData) -> int:
        """Creates and stores a new credentialIssuingData

        Args:
            credentialIssuingData (Database.Entities.CredentialIssuingData): CredentialIssuingData which will be stored

        Returns:
            int: The id of the CredentialIssuingData
        """
        credentialIssiungData.creationDate = datetime.now()

        Setup.SQL_Session.add(credentialIssiungData)
        Setup.SQL_Session.commit()
        return credentialIssiungData.id

    def update():
        Setup.SQL_Session.commit()
    
    def get(id) -> CredentialIssuingData:
        """Gets a CredentialIssuingData by id
        
        Args:
            id (int): credentialIssuingData id

        Returns:
            Database.Entities.CredentialIssuingData: The credentialIssuingData
        """
        return Setup.SQL_Session.query(CredentialIssuingData).filter(CredentialIssuingData.id == id).first()

    def getByCredentialAndAgent(credentialId, agentId) -> CredentialIssuingData:
        """Returns the credentialIssuingData by the given credential id and agent id

        Args:
            credentialId (int): The credential Id
            agentId (int): The agent Id

        Returns:
            Database.Entities.CredentialIssuingData: The credentialIssuingData
        """
        return Setup.SQL_Session.query(CredentialIssuingData).filter(
            CredentialIssuingData.credential_id == credentialId and CredentialIssuingData.agent_id == agentId
            ).first()