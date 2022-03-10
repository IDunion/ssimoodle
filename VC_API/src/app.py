from server.server import Server
from database.database import Database
from server.logger import logging

if __name__  == "__main__":
    logging.info("Starting server...")
    Database.run()

    server = Server()
    server.run()