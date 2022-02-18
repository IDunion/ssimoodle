from datetime import datetime 
from database.entities.credential import Credential, Status
from database.setup import Setup

class CredentialHandler():
    def add(credential):
        """Creates and stores a new credential

        Args:
            credential (Database.Entities.Credential): Credential which will be stored

        Returns:
            int: The id of the credential
        """
        credential.creationDate = datetime.now()
        credential.status = Status.Created.value

        Setup.SQL_Session.add(credential)
        Setup.SQL_Session.commit()
        return credential.id
    
    def get(id):
        """Gets a credential by id
        
        Args:
            id (int): credential id

        Returns:
            Database.Entities.Credential: The credential
        """
        return Setup.SQL_Session.query(Credential).filter(Credential.id == id).first()

    def getByCourseId(courseID):
        """Returns all credential by the given course id

        Args:
            courseID (int): The course Id

        Returns:
            List(Database.Entities.Credential): List of credentials
        """
        return Setup.SQL_Session.query(Credential).filter(Credential.lms_course_id == courseID).all()

    # def getAll():
    #     return Setup.SQL_Session.query(Credential).all()