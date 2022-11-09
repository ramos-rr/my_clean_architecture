import pytest
from .find_user import FindUser
from src.infra.repo.test import UserRepositorySpy
from faker import Faker
from ...infra.errors import NoResultFoundError

fake = Faker()
fake_username = fake.name()
fake_user_id = fake.random_number(digits=5)


def test_find_user_by_user_id():
    """ Test to assess find by user ID"""
    repo = UserRepositorySpy(user_id=fake_user_id)
    find = FindUser(repo)
    name = find.by_user_id(user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id


def test_find_user_by_username():
    """ Test to assess find by username"""
    repo = UserRepositorySpy(usename=fake_username)
    find = FindUser(repo)
    name = find.by_username(username=fake_username)
    assert name["data"][0].username == fake_username


def test_find_user_by_user_id_and_username():
    """ Test to assess find by user ID and username"""
    repo = UserRepositorySpy(usename=fake_username, user_id=fake_user_id)
    find = FindUser(repo)
    name = find.by_user_id_and_username(username=fake_username, user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert name["data"][0].username == fake_username


def test_find_user_generic_error():
    with pytest.raises(Exception):
        repo = UserRepositorySpy()
        find = FindUser(repo)
        query = find.by_user_id_and_username(username=fake_user_id)
        print(query)


def test_find_user_by_id_no_result_found_error():
    repo = UserRepositorySpy()
    find = FindUser(repo)
    query = find.by_user_id(fake_user_id + 1)
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]


def test_find_user_by_username_no_result_found_error():
    repo = UserRepositorySpy()
    find = FindUser(repo)
    query = find.by_username(fake_username)
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]


def test_find_user_by_user_id_and_username_no_result_found_error():
    repo = UserRepositorySpy()
    find = FindUser(repo)
    query = find.by_user_id_and_username(user_id=9999999, username='aaa')
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]
