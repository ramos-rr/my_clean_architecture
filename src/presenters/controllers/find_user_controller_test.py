from .find_user_controller import FindUserController
from src.data.find_user import FindUser
from src.infra.repo.test import UserRepositorySpy
from src.presenters.helpers import HttpRequest
from faker import Faker

# Create Fake values
fake = Faker()
fake_username = fake.name()
fake_user_id = fake.random_number(digits=5)

# Instantiate User Repository Spy with user_id and username
user_repo_spy = UserRepositorySpy(user_id=fake_user_id, usename=fake_username)

# Instantiate find user use case so serve as user finder
find_user_use_case = FindUser(user_repository=user_repo_spy)

# Instantiate find user controller to perform tests
find_user_controller = FindUserController(find_user_use_case=find_user_use_case)


def test_handle_by_user_id_status_code_200():
    """ test handle method using only user id """
    http_request = HttpRequest(query={"user_id": fake_user_id})
    response = find_user_controller.handle(http_request=http_request)
    print(response)

    # Testing output
    assert response.status_code == 200
    assert type(response.body[0]).__name__ == 'Users'
    assert response.body[0].id == fake_user_id


def test_handle_by_username_status_code_200():
    """ test handle method using only username """
    http_request = HttpRequest(query={"username": fake_username})
    response = find_user_controller.handle(http_request=http_request)
    print(response)

    # Testing output
    assert response.status_code == 200
    assert type(response.body[0]).__name__ == 'Users'
    assert response.body[0].username == fake_username


def test_handle_by_user_id_and_username_status_code_200():
    """ test handle method using user ID and username """
    http_request = HttpRequest(query={"user_id": fake_user_id, "username": fake_username})
    response = find_user_controller.handle(http_request=http_request)
    print(response)

    # Testing output
    assert response.status_code == 200
    assert type(response.body[0]).__name__ == 'Users'
    assert response.body[0].id == fake_user_id
    assert response.body[0].username == fake_username


def test_hadle_status_code_422():
    """ test handle method to check return of status code 422 """
    http_request = HttpRequest(query={"user_id": fake_user_id + 1, "username": fake_username})
    response = find_user_controller.handle(http_request=http_request)

    # Testing output
    assert response.status_code == 422
    assert response.body["detail"]


def test_hadle_status_code_400():
    """ test handle method to check return of status code 400 """
    http_request = HttpRequest()
    response = find_user_controller.handle(http_request=http_request)
    print(response)

    # Testing output
    assert response.status_code == 400
    assert "detail" in response.body.keys()
