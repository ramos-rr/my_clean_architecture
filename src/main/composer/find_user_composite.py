from typing import Type
from src.data.find_user import FindUser
from src.infra.repo import UserRepository, PetRepository
from src.presenters.controllers import FindUserController
from src.presenters.interface import RouteInterface


def find_user_composer() -> Type[RouteInterface]:
    """
    Function to instantiate all modules for find user use case
    :return: Route HTTP REQUEST
    """

    user_repo = UserRepository()
    pet_repo = PetRepository()
    find_user_usecase = FindUser(user_repository=user_repo, pet_repository=pet_repo)
    find_user_router = FindUserController(find_user_use_case=find_user_usecase)

    return find_user_router
