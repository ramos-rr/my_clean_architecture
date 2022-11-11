from src.infra.repo.test import UserRepositorySpy
from .register_user_controller import RegisterUserController
from src.data.register_user import RegisterUser
from faker import Faker
from src.presenters.helpers import HttpRequest

# set mock up
fake = Faker()
fake_username = fake.name()
fake_password = f'{fake.word()}{fake.random_number(digits=2)}'

# Set up for tests
user_repo = UserRepositorySpy()
register_user_usecase = RegisterUser(user_repository=user_repo)
register_user_controller = RegisterUserController(register_user_usecase=register_user_usecase)


def test_handle_status_200():
    http_request = HttpRequest(body={"username": fake_username, "password": fake_password})
    response = register_user_controller.route(http_request=http_request)
    assert response.status_code == 200


def test_handle_status_422():
    http_request = HttpRequest(body={"username": fake_username, "password": 'testeabc'})
    response = register_user_controller.route(http_request=http_request)
    assert response.status_code == 422


def test_handle_status_400():
    http_request = HttpRequest()
    response = register_user_controller.route(http_request=http_request)
    assert response.status_code == 400
