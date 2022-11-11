from .register_pet_controller import RegisterPetController
from src.infra.repo.test import UserRepositorySpy, PetRepositorySpy
from src.data.register_pet import RegisterPet
from src.presenters.helpers import HttpRequest
from faker import Faker


# Set up mock variables
fake = Faker()
fake_pet_name = fake.first_name()
fake_pet_age = fake.random_number(digits=1)
fake_user_id = fake.random_number(digits=5)
fake_specie = 'dog'

# Set up instancies
user_repo = UserRepositorySpy(user_id=fake_user_id)
pet_repository = PetRepositorySpy()
register_pet_usecase = RegisterPet(pet_repository=pet_repository, user_repository=user_repo)


def test_register_pet_controller_handle_status_200():
    register_pet_controller = RegisterPetController(register_pet_usecase=register_pet_usecase)
    http_request = HttpRequest(
        body={"petname": fake_pet_name, "specie": fake_specie, "age": fake_pet_age, "user_id": fake_user_id}
    )
    response = register_pet_controller.route(http_request=http_request)
    assert response.status_code == 200


def test_register_pet_controller_handle_status_422():
    register_pet_controller = RegisterPetController(register_pet_usecase=register_pet_usecase)
    http_request = HttpRequest(
        body={"petname": fake_pet_name, "specie": fake_specie, "age": fake_pet_age, "user_id": fake_user_id + 1}
    )
    response = register_pet_controller.route(http_request=http_request)
    assert response.status_code == 422


def test_register_pet_controller_handle_status_400():
    register_pet_controller = RegisterPetController(register_pet_usecase=register_pet_usecase)
    http_request = HttpRequest()
    response = register_pet_controller.route(http_request=http_request)
    assert response.status_code == 400
