from sqlalchemy.ext.declarative import declarative_base

class Setup:
    Base = declarative_base()
    SQL_Session = None