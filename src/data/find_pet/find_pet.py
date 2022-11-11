from typing import Dict, List
from src.domain import Pets
from src.domain.use_cases import FindPetInterface
from src.data.interfaces import PetRepositoryInterface as PetRepository


class FindPet(FindPetInterface):
    """ Class to manage usecase FindPet """

    def __init__(self, pet_repository: [PetRepository]):
        self.pet_repository = pet_repository

    def by_pet_id(self, pet_id: int = None) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using PET ID as parameter
        :param pet_id: Pet ID
        :return: Dictionary with operation success message along with a single query result
        """
        try:
            response = self.pet_repository.select_pet(pet_id=pet_id)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}

    def by_user_id(self, user_id: int = None) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using its OWNER ID as parameter
        :param user_id: Onwe ID -> UserID
        :return: Dictionary with operation success message along with the query result.
        NOTE: Can return more than one pet in case more multiple pets are linked to the same owner
        """
        try:
            response = self.pet_repository.select_pet(user_id=user_id)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}

    def by_pet_id_and_user_id(self, pet_id: int = None, user_id: int = None) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using PET ID and its OWNER ID as parameters
        :param pet_id: Pet ID
        :param user_id: Pet ID
        :return: Dictionary with operation success message along with a silngle query result.
        """
        try:
            response = self.pet_repository.select_pet(pet_id=pet_id, user_id=user_id)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}
