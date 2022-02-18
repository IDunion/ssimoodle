from server.server import Server
from database.database import Database
from server.logger import logger

if __name__  == "__main__":
    logger.info("Starting server...")
    Database.run()
    server = Server()
    server.run()