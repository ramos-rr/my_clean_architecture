from typing import Dict, List
from src.domain import Users
from src.domain.use_cases.find_user import FindUserInterface
from src.data.interfaces import UserRepositoryInterface as UserRepository


class FindUser(FindUserInterface):
    """ Class to perform FindUser usecase"""

    def __init__(self, user_repository: [UserRepository]):
        self.user_repository = user_repository

    def by_user_id(self, user_id: int) -> Dict[bool, List[Users]]:
        """
        Method to find user by its ID
        :param user_id: User's ID
        :return: Dictionary with a success message and the User
        """
        response = None
        try:
            response = self.user_repository.select_user(user_id=user_id)
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
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}
