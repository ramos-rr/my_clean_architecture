from src.infra.config import *
from src.infra.entities import *
import os.path


def create_db():
    db_conn = DbConnectionHandler()
    engine = db_conn.get_engine()
    Base.metadata.create_all(engine)
    return Base.metadata.create_all(engine), Users, Pets, DbConnectionHandler


if __name__ == "__main__":
    exist = os.path.isfile("storage.db")
    if not exist:
        create_db()
    else:
        print('DB already exists')
