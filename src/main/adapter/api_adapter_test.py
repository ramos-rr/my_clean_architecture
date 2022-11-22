from src.infra.repo.test import UserRepositorySpy
from src.data.register_user import RegisterUser
from src.presenters.controllers import RegisterUserController
from .api_adapter import flask_adapter
from ...presenters.helpers import HttpRequest
from collections import namedtuple


def test_flask_adapter_with_register_user_controller_status_200():
    http_request_json = namedtuple("RequestMock", "json")
    http_request = HttpRequest(body={"username": "test user name", "password": "abc123"})
    http_json = http_request_json(json=http_request.body)
    user_repo = UserRepositorySpy()
    registe_user_usecase = RegisterUser(user_repository=user_repo)
    handler = RegisterUserController(register_user_usecase=registe_user_usecase)
    fa = flask_adapter(request=http_json, api_route=handler)
    assert fa.status_code == 200
