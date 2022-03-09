from server.server import Server
from database.database import Database
from server.logger import logging
from global_settings import Settings
# from server.services.polling_service import PollingService

if __name__  == "__main__":
    logging.info("Starting server...")
    Database.run()

    # if Settings.agentResponseType == "POLLING": 
    #     PollingService.run()

    server = Server()
    server.run()