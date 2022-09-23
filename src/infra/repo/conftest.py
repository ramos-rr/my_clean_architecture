import pytest
from src.infra.config import DbConnectionHandler
from src.infra.repo import UserRepository
from faker import Faker


@pytest.fixture(scope='session')
def fake():
    fake_fix = Faker()
    return fake_fix


@pytest.fixture(scope='session')
def db_conn():
    db_conn_fix = DbConnectionHandler()
    return db_conn_fix


@pytest.fixture(scope='session')
def engine(db_conn):
    engine_fix = db_conn.get_engine()
    return engine_fix


@pytest.fixture(scope='session')
def repo():
    repo_fix = UserRepository()
    return repo_fix


@pytest.fixture(scope='session')
def name(fake):
    name_fix = fake.name()
    return name_fix


@pytest.fixture(scope='session')
def password(fake):
    password_fix = fake.word()
    return password_fix
