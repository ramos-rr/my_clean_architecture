from typing import Dict
from src.domain import Users
from src.data.interfaces import UserRepositoryInterface as UserRepository
from src.domain.use_cases import RegisterUserInterface


class RegisterUser(RegisterUserInterface):
    """ Class to define user case: Register User """

    def __init__(self, user_repository: [UserRepository]):
        self.user_repository = user_repository

    def register(self, name, password) -> Dict[bool, Users | Exception]:
        """ Register Users usecase
        :param name: Username
        :param password: User password
        :return: Dictionary with information of the process
        """
        # data validation entry will occur inside UserRepository
        response = None
        try:
            response = self.user_repository.insert_user(username=name, password=password)
            return {"success": True, "data": response}
        except Exception as error:
            return {"success": False, "detail": error}
