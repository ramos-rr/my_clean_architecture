from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


class DbConnectionHandler:

    def __init__(self):
        self.__connection_string = config('DATABASE_STRING')  # This string is need by sqlalchemy
        self.session = None

    def get_engine(self):
        """
        Create a connection to DB
        :return: connection engine
        """
        engine = create_engine(self.__connection_string)
        return engine

    # Define a method to enter DB to garantee some levels of security
    def __enter__(self):
        engine = self.get_engine()
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
