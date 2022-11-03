from abc import ABC, abstractmethod
from typing import List
from src.domain.models import Pets


class PetRepositoryInterface(ABC):
    """
    Interface Class to PET REPOSITORY
    """
    @abstractmethod
    def insert_pet(self, petname: str, specie: str, age: int, user_id: int) -> Pets:
        """
        Abstract Method to insert new pet
        :param petname: Pet name
        :param specie: Pet specie (from AnimalTypes list)
        :param age: Pet age
        :param user_id: Pet owner id
        :return: Class Pets (domain)
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def select_pet(self, pet_id=None, user_id=None) -> List[Pets]:
        """
        Abstract Method to select one or more pets from DB
        :param pet_id: Pet ID
        :param user_id: Pet owner ID
        :return: List of PETS
        """
        raise NotImplementedError("Method not implemented")
