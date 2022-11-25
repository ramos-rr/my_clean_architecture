from typing import Type
from src.data.find_pet import FindPet
from src.infra.repo import PetRepository
from src.presenters.controllers import FindPetController
from src.presenters.interface import RouteInterface


def find_pet_composer() -> Type[RouteInterface]:
    """
    Function to instantiate all modules for find pet use case
    :return: Route HTTP REQUEST
    """

    pet_repo = PetRepository()
    find_pet_usecase = FindPet(pet_repository=pet_repo)
    find_pet_route = FindPetController(find_pet_usecase=find_pet_usecase)

    return find_pet_route
