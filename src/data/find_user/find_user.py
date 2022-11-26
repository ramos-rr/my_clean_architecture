from typing import Dict, List, Type
from src.domain import Users
from src.domain.use_cases.find_user import FindUserInterface
from src.data.interfaces import UserRepositoryInterface as UserRepository
from src.data.interfaces import PetRepositoryInterface as PetRepository


class FindUser(FindUserInterface):
    """ Class to perform FindUser usecase"""

    def __init__(self, user_repository: Type[UserRepository], pet_repository: Type[PetRepository]):
        self.user_repository = user_repository
        self.pet_repository = pet_repository

    def by_user_id(self, user_id: int) -> Dict[bool, List[Users]]:
        """
        Method to find user by its ID
        :param user_id: User's ID
        :return: Dictionary with a success message and the User
        """
        response = None
        try:
            response = self.user_repository.select_user(user_id=user_id)
            pet = self.__get_pet(response)
            response.append(pet)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}

    def by_username(self, username: str) -> Dict[bool, List[Users]]:
        """
        Method to find user by its username
        :param username: User name
        :return: Dictionary with a success message and the User
        """
        response = None
        try:
            response = self.user_repository.select_user(username=username)
            pet = self.__get_pet(response)
            response.append(pet)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}

    def by_user_id_and_username(self, user_id: int, username: str) -> Dict[bool, List[Users]]:
        """
        Method to find user by its User ID and username
        :param user_id: User ID
        :param username: User name
        :return: Dictionary with a success message and the User
        """
        response = None
        try:
            response = self.user_repository.select_user(user_id=user_id, username=username)
            pet = self.__get_pet(response)
            response.append(pet)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}

    def __get_pet(self, response):
        """
        Private method to find if queried user owns one or more pets
        :param response: response from caller method
        :return: List that can contain one or more pets
        """
        try:
            positive_user_id = response[0].id
            pet = self.pet_repository.select_pet(user_id=positive_user_id)
        except:
            pet = []
        return pet
