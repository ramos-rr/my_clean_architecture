from typing import Dict
from src.domain import Pets
from src.data.find_user import FindUser
from src.data.interfaces import PetRepositoryInterface as PetRepository
from src.data.interfaces import UserRepositoryInterface as UserRepository
from src.domain.use_cases import RegisterPetInterface


class RegisterPet(RegisterPetInterface):

    def __init__(self, pet_repository: [PetRepository], user_repository: [UserRepository]):
        self.user_repository = user_repository
        self.pet_repository = pet_repository

    def register(self, petname: str, specie: str, age: int, user_id: int) -> Dict[bool, Pets] | Dict:
        """
        Abstractmethod to register pet usecase
        :param petname: Pet name as string
        :param specie: Pet specie as string (Must be inside Enum allowed specie)
        :param age: Pet age
        :param user_id: Pet owner ID
        :return: Dictionary with a success message and Pets models
        """
        response = None
        query_user = self.__find_user(user_id)
        if query_user["success"]:
            try:
                response = self.pet_repository.insert_pet(petname=petname, specie=specie, age=age, user_id=user_id)
                return {"success": True, "data": response}
            except Exception as error:
                return {"success": False, "detail": error}
        else:
            response = query_user["detail"]
            return {"success": False, "detail": response}

    def __find_user(self, user_id: int):
        """
        Private method to check if a User exists
        :param user_id: Pet owner ID
        """
        response = FindUser(self.user_repository, self.pet_repository).by_user_id(user_id=user_id)
        return response
