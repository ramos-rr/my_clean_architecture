from typing import Dict
from abc import ABC, abstractmethod
from src.domain import Users


class FindUserInterface(ABC):
    """ Class Interface to Find User use case """

    @abstractmethod
    def by_user_id(self, user_id: int) -> Dict[bool, Users]:
        """
        Abstractmethod to find user by its ID
        :param user_id: User ID
        :return: Dictionary with a success message and the User
        """
        raise NotImplementedError("You must implement this method")

    @abstractmethod
    def by_username(self, username: str) -> Dict[bool, Users]:
        """
        Abstractmethod to find user by its username
        :param username: User name
        :return: Dictionary with a success message and the User
        """
        raise NotImplementedError("You must implement this method")

    @abstractmethod
    def by_user_id_and_username(self, user_id: int, username: str) -> Dict[bool, Users]:
        """
        Abstractmethod to find user by its User ID and username
        :param user_id: User ID
        :param username: User name
        :return: Dictionary with a success message and the User
        """
        raise NotImplementedError("You must implement this method")
