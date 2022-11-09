from typing import Dict
from src.domain import Pets
from abc import ABC, abstractmethod


class RegisterPetInterface(ABC):
    """ Class Interface to Register Pet usecase """

    @abstractmethod
    def register(self, petname, specie, age, user_id) -> Dict[bool, Pets]:
        """
        Abstractmethod to register pet usecase
        :param petname: Pet name as string
        :param specie: Pet specie as string (Must be inside Enum allowed specie)
        :param age: Pet age
        :param user_id: Pet owner ID
        :return: Dictionary with a success message and Pets models
        """
        raise NotImplementedError("You must implement this method")
