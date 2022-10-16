import random

import pytest
from src.infra.config import DbConnectionHandler
from src.infra.repo import UserRepository
from faker import Faker
from src.infra.repo.pet_repository import PetRepository


# GENERAL FIXTURE FEATURES
@pytest.fixture(scope='session')
def fake():
    fake_fix = Faker()
    return fake_fix


@pytest.fixture(scope='session')
def engine():
    db_conn_fix = DbConnectionHandler()
    engine_fix = db_conn_fix.get_engine()
    return engine_fix


# FIXTURE FOR USER_REPOSOSITORY TESTS
@pytest.fixture(scope='session')
def userrepo():
    repo_fix = UserRepository()
    return repo_fix


@pytest.fixture(scope='session')
def username(fake):
    username_fix = fake.name()
    return username_fix


@pytest.fixture(scope='session')
def user_id(fake):
    user_id_fix = fake.random_number(digits=5)
    return user_id_fix


@pytest.fixture(scope='session')
def password(fake):
    password_fix = f'{fake.word()}{fake.random_number(digits=2)}'
    return password_fix


@pytest.fixture(scope='session')
def db_conn():
    with DbConnectionHandler() as session_fixture:
        return session_fixture


# FIXTURE FOR PET_REPOSITORY TESTS
@pytest.fixture(scope='session')
def petrepo():
    pet_fix = PetRepository()
    return pet_fix


@pytest.fixture(scope='session')
def petname(fake):
    pet_name_fix = fake.first_name()
    return pet_name_fix


@pytest.fixture(scope='session')
def specie():
    from src.infra.entities.pets import AnimalTypes
    specie_list = AnimalTypes._member_names_
    specie_fix = random.choice(specie_list)
    del specie_list
    return specie_fix


@pytest.fixture(scope='session')
def age(fake):
    age_fix = fake.random_number(digits=1)
    return age_fix


@pytest.fixture(scope='session')
def pet_id(fake):
    pet_id_fix = fake.random_number(digits=5)
    return pet_id_fix
