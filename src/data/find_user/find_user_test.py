import pytest
from .find_user import FindUser
from src.infra.repo.test import UserRepositorySpy, PetRepositorySpy
from faker import Faker
from ...infra.errors import NoResultFoundError

fake = Faker()
fake_username = fake.name()
fake_user_id = fake.random_number(digits=5)

userrepo = UserRepositorySpy(user_id=fake_user_id, usename=fake_username)
petrepo_negative = PetRepositorySpy()
find_user_usecase_negative = FindUser(user_repository=userrepo, pet_repository=petrepo_negative)
petrepo_positive = PetRepositorySpy(user_id=fake_user_id)
find_user_usecase_positive = FindUser(user_repository=userrepo, pet_repository=petrepo_positive)


def test_find_user_by_user_id_not_a_pet_owner():
    """ Test to assess find by user ID"""
    name = find_user_usecase_negative.by_user_id(user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert len(name["data"][1]) == 0


def test_find_user_by_user_id_is_a_pet_owner():
    """ Test to assess find by user ID"""
    name = find_user_usecase_positive.by_user_id(user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert name["data"][1][0].user_id == fake_user_id


def test_find_user_by_username_not_a_pet_owner():
    """ Test to assess find by username"""
    name = find_user_usecase_negative.by_username(username=fake_username)
    assert name["data"][0].username == fake_username
    assert len(name["data"][1]) == 0


def test_find_user_by_username_is_a_pet_owner():
    """ Test to assess find by username"""
    name = find_user_usecase_positive.by_username(username=fake_username)
    assert name["data"][0].username == fake_username
    assert len(name["data"][1]) != 0
    assert name["data"][1][0].user_id == name["data"][0].id


def test_find_user_by_user_id_and_username_not_a_pet_owner():
    """ Test to assess find by user ID and username"""
    name = find_user_usecase_negative.by_user_id_and_username(username=fake_username, user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert name["data"][0].username == fake_username
    assert len(name["data"][1]) == 0


def test_find_user_by_user_id_and_username_is_a_pet_owner():
    """ Test to assess find by user ID and username"""
    name = find_user_usecase_positive.by_user_id_and_username(username=fake_username, user_id=fake_user_id)
    assert name["data"][0].id == fake_user_id
    assert name["data"][0].username == fake_username
    assert len(name["data"][1]) != 0
    assert name["data"][1][0].user_id == name["data"][0].id


def test_find_user_generic_error():
    with pytest.raises(Exception):
        repo = UserRepositorySpy()
        find = FindUser(repo, petrepo_negative)
        query = find.by_user_id_and_username(username=fake_user_id)
        print(query)


def test_find_user_by_id_no_result_found_error():
    query = find_user_usecase_negative.by_user_id(fake_user_id + 1)
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]


def test_find_user_by_username_no_result_found_error():
    query = find_user_usecase_negative.by_username(fake_username + 'a')
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]


def test_find_user_by_user_id_and_username_no_result_found_error():
    query = find_user_usecase_negative.by_user_id_and_username(user_id=9999999, username='aaa')
    # Assertion expect to raise NoResultFound error
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
    assert not query["success"]
