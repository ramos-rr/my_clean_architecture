import pytest
from .find_user import FindUser
from src.infra.repo.test import UserRepositorySpy
from faker import Faker

fake = Faker()
fake_username = fake.name()
fake_user_id = fake.random_number(digits=5)


def test_find_user_by_user_id():
    """ Test to assess find by user ID"""
    repo = UserRepositorySpy()
    find = FindUser(repo)
    name = find.by_user_id(user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id


def test_find_user_by_username():
    """ Test to assess find by username"""
    repo = UserRepositorySpy()
    find = FindUser(repo)
    name = find.by_username(username=fake_username)
    assert name["data"][0].username == fake_username


def test_find_user_by_user_id_and_username():
    """ Test to assess find by user ID and username"""
    repo = UserRepositorySpy()
    find = FindUser(repo)
    name = find.by_user_id_and_username(username=fake_username, user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert name["data"][0].username == fake_username


def test_find_user_error():
    with pytest.raises(Exception):
        repo = UserRepositorySpy()
        find = FindUser(repo)
        find.by_user_id_and_username(username=fake_user_id)
