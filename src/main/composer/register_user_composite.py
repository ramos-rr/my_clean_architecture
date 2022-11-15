from src.presenters.interface import RouteInterface
from src.presenters.controllers import RegisterUserController
from src.data.register_user import RegisterUser
from src.infra.repo import UserRepository


def register_user_composer() -> RouteInterface:
    """
    Function to compose register user
    :param: None
    :return: Object with register user route
    """

    user_repo = UserRepository()
    register_user_usecase = RegisterUser(user_repository=user_repo)
    register_user_route = RegisterUserController(register_user_usecase=register_user_usecase)

    return register_user_route
