from typing import Type
from src.infra.config import DbConnectionHandler
from src.domain.models import Users
from src.infra.entities import Users as UsersModel


class UserRepository:
    """ Class to manage Users """

    @classmethod
    def insert_user(cls, database: Type[DbConnectionHandler], name: str, password: str) -> Users:
        """
        Method to insert new user
        params: name: New User's name,
        params: password: New user's password
        """

        with database as db_conn:
            try:
                new_user = UsersModel(name=name, password=password)
                db_conn.session.add(new_user)
                db_conn.session.commit()
                return Users(
                    id=new_user.id, name=new_user.name, password=new_user.password
                )
            except:
                db_conn.session.rollback()
            finally:
                db_conn.session.close()
