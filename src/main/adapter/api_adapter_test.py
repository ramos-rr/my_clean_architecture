from src.infra.repo.test import UserRepositorySpy, PetRepositorySpy
from src.data.register_user import RegisterUser
from src.presenters.controllers import RegisterUserController, FindUserController, RegisterPetController, \
    FindPetController
from .api_adapter import flask_adapter
from ...data.find_pet import FindPet
from ...data.find_user import FindUser
from ...data.register_pet import RegisterPet
from ...presenters.helpers import HttpRequest
from collections import namedtuple


def test_flask_adapter_with_register_user_controller_status_200():
    http_request_json = namedtuple("RequestMock", "json")
    http_request = HttpRequest(body={"username": "test user name", "password": "abc123"})
    http_json = http_request_json(json=http_request.body)
    user_repo = UserRepositorySpy()
    registe_user_usecase = RegisterUser(user_repository=user_repo)
    router = RegisterUserController(register_user_usecase=registe_user_usecase)
    fa = flask_adapter(request=http_json, api_route=router)
    assert fa.status_code == 200


def test_flask_adapter_with_find_user_controller_status_200():
    # set up mocks
    request_mock = namedtuple("RequestMock", "args")

    # instantiate mocks
    http_query = request_mock(args={"user_id": 999, "username": 'Adapter Test'})

    user_repo = UserRepositorySpy(user_id=999, usename='Adapter Test')
    pet_repo = PetRepositorySpy()
    find_user_usecase = FindUser(user_repository=user_repo, pet_repository=pet_repo)
    router = FindUserController(find_user_use_case=find_user_usecase)
    fa = flask_adapter(request=http_query, api_route=router)
    assert fa.status_code == 200


def test_flask_adapter_with_register_pet_controller_status_200():
    http_request_json = namedtuple("RequestMock", "json")
    http_request = HttpRequest(body={"petname": "queer", "specie": "dog", "age": 9, "user_id": 1500})
    http_json = http_request_json(json=http_request.body)
    user_repo = UserRepositorySpy(user_id=1500)
    pet_repo = PetRepositorySpy()
    register_pet_usecase = RegisterPet(pet_repository=pet_repo, user_repository=user_repo)
    router = RegisterPetController(register_pet_usecase=register_pet_usecase)
    fa = flask_adapter(request=http_json, api_route=router)
    assert fa.status_code == 200


def test_flask_adapter_with_find_pet_controller_status_200():
    # set up mocks
    request_mock = namedtuple("RequestMock", "args")

    # instantiate mocks
    http_query = request_mock(args={"user_id": 1500, "pet_id": 1999})

    pet_repo = PetRepositorySpy(pet_id=1999, user_id=1500)
    find_pet_usecase = FindPet(pet_repository=pet_repo)
    router = FindPetController(find_pet_usecase=find_pet_usecase)
    fa = flask_adapter(request=http_query, api_route=router)
    assert fa.status_code == 200
