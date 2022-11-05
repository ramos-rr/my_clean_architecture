from abc import ABC, abstractmethod
from typing import List
from src.infra.entities import Users


class UserRepositoryInterface(ABC):
    """ Abstract Class to User Repository """

    @abstractmethod
    def insert_user(cls, username: str, password: str) -> Users:
        """
        Abstract Method to insert new user
        params: username: New User's name,
        params: password: New user's password
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def select_user(cls, user_id: int = None, username: str = None) -> List[Users]:
        """
        Abstract Method to select data in user entity by ID and/or Name
        :param user_id: ID of the registry,
        :param username: User name,
        :return: List with Users selected
        """
        raise NotImplementedError("Method not implemented")
