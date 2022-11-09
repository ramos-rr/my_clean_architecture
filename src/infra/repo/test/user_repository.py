from typing import List
from src.data.interfaces import UserRepositoryInterface
from src.domain.models import Users
from src.infra.errors import ErrorManager, NoResultFoundError
from faker import Faker
from datetime import datetime

fake = Faker()
now = datetime.now()


class UserRepositorySpy(UserRepositoryInterface):
    """ Class to mock UserRepository to serve as a test feature in the project """

    def __init__(self,
                 user_id=fake.random_number(digits=5),
                 usename=fake.name(),
                 password='teste123',
                 ):
        self.id = user_id
        self.usename = usename
        self.password = password
        self.register_date = now
        self.session = 'test.test.test'

    def insert_user(self, username: str, password: str) -> Users:
        """
        Method to test insertion of a new user
        params: username: New User's name,
        params: password: New user's password
        """
        username, password = self.__validate_insert_user(username=username, password=password)

        return Users(
            id=fake.random_number(digits=5),
            username=username,
            password=password,
            register_date=now,
            session='test.test.test'  # Instead of provide an engine, this feature offers "test.test.test" to kwon
            # it's a test and wouldn't work with a real DB.
        )

    def select_user(self, user_id: int = None, username: str = None) -> List[Users]:
        """
        Method to test query data in user entity by ID and/or Name
        :param user_id: ID of the registry,
        :param username: User name,
        :return: List with Users selected
        """

        self.__validate_select_user(user_id, username)

        if user_id and not username:
            try:
                if user_id == self.id:
                    return [Users(
                        id=self.id,
                        username=self.usename,
                        password=self.password,
                        register_date=self.register_date,
                        session=self.session,
                    )]
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

        elif not user_id and username:
            try:
                if username == self.usename:
                    return [Users(
                        id=self.id,
                        username=self.usename,
                        password=self.password,
                        register_date=self.register_date,
                        session=self.session,
                    )]
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

        elif user_id and username:
            try:
                if username == self.usename and user_id == self.id:
                    return [Users(
                        id=self.id,
                        username=self.usename,
                        password=self.password,
                        register_date=self.register_date,
                        session=self.session,
                    )]
                else:
                    raise Exception
            except Exception:
                raise NoResultFoundError(message='No row was found when one was required', code=None)

    @classmethod
    def __validate_insert_user(cls, username, password):
        ErrorManager.validate_insert_user(username=username, password=password)
        return username, password

    @classmethod
    def __validate_select_user(cls, user_id, username):
        ErrorManager.validate_select_user(username=username, user_id=user_id)
