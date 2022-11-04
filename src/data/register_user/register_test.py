import pytest
from faker import Faker
from .register import RegisterUser
from src.infra.repo.test import UserRepositorySpy

fake = Faker()


def test_register():
    """ Test register user """
    register = RegisterUser(UserRepositorySpy)
    name = fake.name()
    password = f'{fake.word()}{fake.random_number(digits=2)}'
    new_user = register.register(name=name, password=password)
    print(new_user)
    assert new_user["data"].username == name
    assert new_user["data"].password == password
    assert new_user["data"].session == 'test.test.test'


def test_register_error():
    """ Test register user error"""
    with pytest.raises(Exception):
        register = RegisterUser(UserRepositorySpy)
        new_user = register.register(name=fake.name(), password=f'{fake.word()}')
        print(new_user)
        assert new_user["success"]
