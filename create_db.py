from src.infra.config import *
from src.infra.entities import *


def create_db():
    db_conn = DbConnectionHandler()
    engine = db_conn.get_engine()
    Base.metadata.create_all(engine)
    return Base.metadata.create_all(engine), Users, Pets, DbConnectionHandler
