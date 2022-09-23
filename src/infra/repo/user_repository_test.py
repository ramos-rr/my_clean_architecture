import pytest

from src.infra.repo import UserRepository
from faker import Faker

fake = Faker()
repo = UserRepository()


def test_insert_user():
    name = fake.name()
    password = fake.word()

    repo.insert_user(name, password)
