from abc import ABC, abstractmethod
from typing import Dict, List
from src.domain import Pets


class FindPetInterface(ABC):
    """ Abstractclass to manage usecase FindPet """

    @abstractmethod
    def by_pet_id(self, pet_id: int) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using PET ID as parameter
        :param pet_id: Pet ID
        :return: Dictionary with operation success message along with a single query result
        """
        raise NotImplementedError

    @abstractmethod
    def by_user_id(self, user_id: int) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using its OWNER ID as parameter
        :param user_id: Onwe ID -> UserID
        :return: Dictionary with operation success message along with the query result.
        NOTE: Can return more than one pet in case more multiple pets are linked to the same owner
        """
        raise NotImplementedError

    @abstractmethod
    def by_pet_id_and_user_id(self, pet_id: int, user_id: int) -> Dict[bool, List[Pets] | any]:
        """
        Method to find Pet in DB using PET ID and its OWNER ID as parameters
        :param pet_id: Pet ID
        :param user_id: Pet ID
        :return: Dictionary with operation success message along with a silngle query result.
        """
        raise NotImplementedError
