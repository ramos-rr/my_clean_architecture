import random
import pytest
from faker import Faker
from src.infra.entities.pets import AnimalTypes
from src.infra.repo.test import PetRepositorySpy, UserRepositorySpy


@pytest.fixture(scope='session')
def fake():
    fake_fix = Faker()
    return fake_fix


@pytest.fixture(scope='session')
def pet_repo():
    repo_fix = PetRepositorySpy()
    return repo_fix


@pytest.fixture(scope='session')
def user_repo():
    repo_fix = UserRepositorySpy()
    return repo_fix


@pytest.fixture(scope='session')
def petname(fake):
    pet_name_fix = fake.first_name()
    return pet_name_fix


@pytest.fixture(scope='session')
def specie():
    specie_list = AnimalTypes._member_names_
    specie_fix = random.choice(specie_list)
    del specie_list
    return specie_fix


@pytest.fixture(scope='session')
def age(fake):
    age_fix = fake.random_number(digits=1)
    return age_fix


@pytest.fixture(scope='session')
def user_id(fake):
    user_id_fix = fake.random_number(digits=5)
    return user_id_fix
