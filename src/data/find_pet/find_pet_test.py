from .find_pet import FindPet
from src.infra.repo.test import PetRepositorySpy
from faker import Faker
from ...infra.errors import NoResultFoundError

fake = Faker()
fake_petname = fake.name()
fake_pet_id = fake.random_number(digits=5)
fake_user_id = fake.random_number(digits=5)


def test_find_pet_by_pet_id():
    pet_repo = PetRepositorySpy(pet_id=fake_pet_id)
    find = FindPet(pet_repository=pet_repo)
    query = find.by_pet_id(pet_id=fake_pet_id)
    assert query["success"]
    assert query["data"][0].id == fake_pet_id


def test_find_pet_by_user_id():
    pet_repo = PetRepositorySpy(user_id=fake_user_id)
    find = FindPet(pet_repository=pet_repo)
    query = find.by_user_id(user_id=fake_user_id)
    assert query["success"]
    assert query["data"][0].user_id == fake_user_id


def test_find_pet_by_pet_id_and_user_id():
    pet_repo = PetRepositorySpy(pet_id=fake_pet_id, user_id=fake_user_id)
    find = FindPet(pet_repository=pet_repo)
    query = find.by_pet_id_and_user_id(pet_id=fake_pet_id, user_id=fake_user_id)
    assert query["success"]
    assert query["data"][0].id == fake_pet_id
    assert query["data"][0].user_id == fake_user_id


def test_find_pet_error():
    pet_repo = PetRepositorySpy()
    find = FindPet(pet_repo)
    query = find.by_pet_id()
    assert not query['success']


def test_find_pet_no_result_found_error():
    pet_repo = PetRepositorySpy()
    find = FindPet(pet_repo)
    query = find.by_pet_id(99999)
    assert type(query['detail']).__name__ == NoResultFoundError.__name__
