from src.infra.config import *
from decouple import config
import os.path


class CreateDataBase:
    """ Class to create a SQLITE DATABSE IN CASE IT DOESN'T EXIST """

    @classmethod
    def create_db(cls) -> None:
        if not cls.__get_database_string():
            db_conn = DbConnectionHandler()
            engine = db_conn.get_engine()
            Base.metadata.create_all(engine)
            return None

    @classmethod
    def __get_database_string(cls) -> bool:
        database_string = os.path.isfile(config("DATABASE_STRING"))
        return database_string
