from src.infra.repo.test import UserRepositorySpy
from src.data.register_user import RegisterUser
from src.presenters.controllers import RegisterUserController  # FindUserController
from .api_adapter import flask_adapter
# from ...data.find_user import FindUser
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


# def test_flask_adapter_with_find_user_controller_status_200():
#     http_request_json = namedtuple("RequestMock", "json")
#     http_request = HttpRequest(query={"username": "test find user", "user_id": 999})
#     http_json = http_request_json(json=http_request.query)
#     user_repo = UserRepositorySpy()
#     find_user_usecase = FindUser(user_repository=user_repo)
#     router = FindUserController(find_user_use_case=find_user_usecase)
#     fa = flask_adapter(request=http_json, api_route=router)
#     assert fa.status_code == 200
