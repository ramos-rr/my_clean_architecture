from typing import Type

from src.data.register_pet import RegisterPet
from src.infra.repo import PetRepository, UserRepository
from src.presenters.controllers import RegisterPetController
from src.presenters.interface import RouteInterface


def register_pet_composer() -> Type[RouteInterface]:
    """
    Function to instantiate all modules for register pet use case
    :return: Route HTTP REQUEST
    """

    pet_repo = PetRepository()
    user_repo = UserRepository()
    register_pet_usecase = RegisterPet(pet_repository=pet_repo, user_repository=user_repo)
    register_pet_router = RegisterPetController(register_pet_usecase=register_pet_usecase)

    return register_pet_router
