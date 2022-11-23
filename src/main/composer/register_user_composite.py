from typing import Type
from src.data.register_user import RegisterUser
from src.infra.repo import UserRepository
from src.presenters.controllers import RegisterUserController
from src.presenters.interface import RouteInterface


# PUT ALL PIECES TOGETHER AND RETURN THE COMPOSER ITSELF
def register_user_composer() -> Type[RouteInterface]:
    """
    Function to compose register user
    :param: None
    :return: Object with register user route
    """

    user_repo = UserRepository()
    register_user_usecase = RegisterUser(user_repository=user_repo)
    register_user_router = RegisterUserController(register_user_usecase=register_user_usecase)

    return register_user_router
