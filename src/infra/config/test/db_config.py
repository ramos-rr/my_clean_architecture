from sqlalchemy import create_engine
from src.infra.config import DbConnectionHandler


class DbConnectionHandlerSpy(DbConnectionHandler):

    def get_engine(self):
        engine = create_engine("sqlite:///storage.test.db")
        return engine
