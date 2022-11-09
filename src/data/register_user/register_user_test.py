import pytest
from faker import Faker
from .register_user import RegisterUser
from src.infra.repo.test import UserRepositorySpy

fake = Faker()


def test_register():
    """ Test register user """
    user_repo = UserRepositorySpy()
    register = RegisterUser(user_repo)  # It calls UserRepositorySpy to receive class Users as response but
    # with no engine, just "test.test.test"
    name = fake.name()
    password = f'{fake.word()}{fake.random_number(digits=2)}'
    new_user = register.register(name=name, password=password)
    assert new_user["data"].username == name
    assert new_user["data"].password == password
    assert new_user["data"].session == 'test.test.test'


def test_register_error():
    """ Test register user error"""
    with pytest.raises(Exception):
        register = RegisterUser(UserRepositorySpy)
        new_user = register.register(name=fake.name(), password=f'{fake.word()}')
        assert new_user["success"]
