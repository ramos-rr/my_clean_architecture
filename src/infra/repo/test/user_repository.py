from typing import List
from src.data.interfaces import UserRepositoryInterface
from src.domain.models import Users
from src.infra.errors import ErrorManager
from faker import Faker
from datetime import datetime

fake = Faker()
now = datetime.now()


class UserRepositorySpy(UserRepositoryInterface):
    """ Class to mock UserRepository to serve as a test feature in the project """

    @classmethod
    def insert_user(cls, username: str, password: str) -> Users:
        """
        Method to test insertion of a new user
        params: username: New User's name,
        params: password: New user's password
        """
        username, password = cls.__validate_insert_user(username=username, password=password)

        return Users(
            id=fake.random_number(digits=5),
            username=username,
            password=password,
            register_date=now,
            session='test.test.test'  # Instead of provide an engine, this feature offers "test.test.test" to kwon
            # it's a test and wouldn't work with a real DB.
        )

    @classmethod
    def select_user(cls, user_id: int = None, username: str = None) -> List[Users]:
        """
        Method to test query data in user entity by ID and/or Name
        :param user_id: ID of the registry,
        :param username: User name,
        :return: List with Users selected
        """

        cls.__validate_select_user(user_id, username)

        if user_id and not username:
            return [Users(
                id=user_id,
                username=fake.name(),
                password='teste123',
                register_date=now,
                session='test.test.test'  # Instead of provide an engine, this feature offers "test.test.test"
                # to kwon it's a test and wouldn't work with a real DB.
            )]

        elif not user_id and username:
            return [Users(
                id=fake.random_number(digits=5),
                username=username,
                password='teste123',
                register_date=now,
                session='test.test.test'  # Instead of provide an engine, this feature offers "test.test.test"
                # to kwon it's a test and wouldn't work with a real DB.
            )]

        elif user_id and username:
            return [Users(
                id=user_id,
                username=username,
                password='teste123',
                register_date=now,
                session='test.test.test'  # Instead of provide an engine, this feature offers "test.test.test"
                # to kwon it's a test and wouldn't work with a real DB.
            )]

    @classmethod
    def __validate_insert_user(cls, username, password):
        ErrorManager.validate_insert_user(username=username, password=password)
        return username, password

    @classmethod
    def __validate_select_user(cls, user_id, username):
        ErrorManager.validate_select_user(username=username, user_id=user_id)
