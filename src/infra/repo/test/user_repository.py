from typing import List
from src.data.interfaces import UserRepositoryInterface
from src.infra.config import DbConnectionHandler
from src.domain.models import Users
from src.infra.entities import Users as UsersEntity
from src.infra.errors import ErrorManager


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

        from faker import Faker
        from datetime import datetime
        fake = Faker()
        now = datetime.now()

        return Users(
            id=fake.random_number(digits=5),
            username=username,
            password=password,
            register_date=now,
            session='test.test.test'
        )

    @classmethod
    def select_user(cls, user_id: int = None, username: str = None) -> List[Users]:
        """
        Select data in user entity by ID and/or Name
        :param user_id: Id of the registry,
        :param username: User name,
        :return: List with Users selected
        """
        # VALIDADE DATA: username and user_id
        cls.__validate_select_user(user_id, username)

        try:
            if user_id and not username:
                with DbConnectionHandler() as db_conn:
                    # DATA = ...sessão.query(Modelo_de_Usuário).filtrado_por(id=user_id_informado).único()
                    data = db_conn.session.query(UsersEntity).filter_by(id=user_id).one()
                    query_data = [data]

            elif not user_id and username:
                with DbConnectionHandler() as db_conn:
                    # DATA = ...sessão.query(Modelo_de_Usuário).filtrado_por(nome=user_name_informado).único()
                    data = db_conn.session.query(UsersEntity).filter_by(username=username).one()
                    query_data = [data]

            elif user_id and username:
                with DbConnectionHandler() as db_conn:
                    # DATA = ...sessão.query(Modelo_de_Usuário).filtrado_por(id=user_id_informado,
                    # nome=user_name_informado).único()
                    data = db_conn.session.query(UsersEntity).filter_by(id=user_id, username=username).one()
                    query_data = [data]

            return query_data

        except Exception as error:
            try:
                error.__getattribute__('code')
            except:
                ErrorManager.database_error(error.args)
            else:
                ErrorManager.database_error(error.args, error.code)
            db_conn.session.rollback()
        finally:
            db_conn.session.close()

    @classmethod
    def __validate_insert_user(cls, username, password):
        ErrorManager.validate_insert_user(username=username, password=password)
        return username, password

    @classmethod
    def __validate_select_user(cls, user_id, username):
        ErrorManager.validate_select_user(username=username, user_id=user_id)
