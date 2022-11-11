from faker import Faker
from .find_pet_controller import FindPetController
from src.infra.repo.test import PetRepositorySpy
from src.data.find_pet import FindPet
from src.presenters.helpers import HttpRequest

# create mocks
fake = Faker()
fake_pet_name = fake.first_name()
fake_pet_id = fake.random_number(digits=5)
fake_user_id = fake.random_number(digits=5)

# create registries to be found
pet_repo_spy = PetRepositorySpy(pet_id=fake_pet_id, user_id=fake_user_id)
find_use_case = FindPet(pet_repo_spy)
find_pet_controller = FindPetController(find_pet_usecase=find_use_case)


def test_handle_by_pet_id_and_user_id_status_code_200():
    http_request = HttpRequest(query={"user_id": fake_user_id, "pet_id": fake_pet_id})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 200
    assert response.body[0].id == fake_pet_id
    assert response.body[0].user_id == fake_user_id


def test_handle_by_pet_id_and_user_id_status_code_4200_error():
    http_request = HttpRequest(query={"user_id": fake_user_id + 1, "pet_id": fake_pet_id + 1})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 422


def test_handle_by_user_id_status_code_200():
    http_request = HttpRequest(query={"user_id": fake_user_id})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 200
    assert response.body[0].user_id == fake_user_id


def test_handle_by_user_id_status_code_422_error():
    http_request = HttpRequest(query={"user_id": fake_user_id + 1})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 422


def test_handle_by_pet_id_code_200():
    http_request = HttpRequest(query={"pet_id": fake_pet_id})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 200
    assert response.body[0].id == fake_pet_id


def test_handle_by_pet_id_code_422_error():
    http_request = HttpRequest(query={"pet_id": fake_pet_id + 1})
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 422


def test_handle_status_code_400_error():
    http_request = HttpRequest()
    response = find_pet_controller.handle(http_request)
    assert response.status_code == 400
