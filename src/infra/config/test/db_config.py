from sqlalchemy import create_engine
from src.infra.config import DbConnectionHandler
from decouple import config


class DbConnectionHandlerSpy(DbConnectionHandler):

    def get_engine(self):
        db_string = config("DATABASE_STRING")
        front, end = db_string.split('.')
        engine = create_engine(front + '.test.' + end)
        return engine
