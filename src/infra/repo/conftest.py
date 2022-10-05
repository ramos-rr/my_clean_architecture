import pytest
from src.infra.config import DbConnectionHandler
from src.infra.repo import UserRepository
from faker import Faker


@pytest.fixture(scope='session')
def fake():
    fake_fix = Faker()
    return fake_fix


@pytest.fixture(scope='session')
def engine():
    db_conn_fix = DbConnectionHandler()
    engine_fix = db_conn_fix.get_engine()
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
def user_id(fake):
    user_id_fix = fake.random_number(digits=5)
    return user_id_fix


@pytest.fixture(scope='session')
def password(fake):
    password_fix = fake.word()
    return password_fix
