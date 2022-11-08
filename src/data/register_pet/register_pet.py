from typing import Dict
from src.domain import Pets
from src.data.find_user import FindUser
from src.data.interfaces import PetRepositoryInterface as PetRepository
from src.data.interfaces import UserRepositoryInterface as UserRepository
from src.domain.use_cases import RegisterPetInterface


class RegisterPet(RegisterPetInterface):

    def __init__(self, pet_repository: PetRepository, user_repository: [UserRepository]):
        self.user_repository = user_repository
        self.pet_repository = pet_repository

    def register(self, petname: str, specie: str, age: int, user_id: int) -> Dict[bool, Pets]:
        """
        Abstractmethod to register pet usecase
        :param petname: Pet name as string
        :param specie: Pet specie as string (Must be inside Enum allowed specie)
        :param age: Pet age
        :param user_id: Pet owner ID
        :return: Dictionary with a success message and Pets models
        """
        response = None
        user = self.__find_user(user_id)
        if user:
            try:
                response = self.pet_repository.insert_pet(petname=petname, specie=specie, age=age, user_id=user_id)
                return {"success": True, "data": response}
            except Exception as error:
                return {"success": False, "detail": error}
        else:
            return {"success": False, "data": response}

    def __find_user(self, user_id: int):
        """
        Private method to check if a User exists
        :param user_id: Pet owner ID
        """
        response = FindUser(self.user_repository).by_user_id(user_id=user_id)
        return response["success"]
