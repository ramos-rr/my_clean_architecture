import pytest
from src.infra.errors import ErrorManager, DatabaseError
from src.infra.config import DbConnectionHandler
from src.infra.config.test import DbConnectionHandlerSpy


def test_get_engine():
    conn = DbConnectionHandler()
    engine = conn.get_engine()
    assert str(engine.url) == conn._DbConnectionHandler__connection_string


def test_enter():
    with DbConnectionHandler() as conn:
        assert conn.session is not None


def test_database_error():
    with pytest.raises(DatabaseError):
        conn = DbConnectionHandlerSpy()
        engine = conn.get_engine()
        try:
            _ = engine.execute("SELECT * FROM users WHERE id='{}';".format(1)).fetchone()
        except Exception as error:
            ErrorManager.database_error(message=error.args, code=error.code)
