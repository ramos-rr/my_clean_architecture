import datetime
from typing import List
from src.infra.config import DbConnectionHandler
from src.domain.models import Users
from src.infra.entities import Users as UsersEntity


class UserRepository:
    """ Class to manage Users """

    @classmethod
    def insert_user(cls, username: str, password: str) -> Users:
        """
        Method to insert new user
        params: username: New User's name,
        params: password: New user's password
        """

        with DbConnectionHandler() as db_conn:
            try:
                new_user = UsersEntity(username=username, password=password, register_date=datetime.datetime.now())
                db_conn.session.add(new_user)
                db_conn.session.commit()
                return Users(
                    id=new_user.id, username=new_user.username, password=new_user.password,
                    register_date=new_user.register_date
                )
            except:
                db_conn.session.rollback()
            finally:
                db_conn.session.close()

    @classmethod
    def select_user(cls, user_id: int = None, username: str = None) -> List[Users]:
        """
        Select data in user entity by ID and/or Name
        :param user_id: Id of the registry,
        :param username: User name,
        :return: List with Users selected
        """
        try:
            query_data = None
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
            print(error.args)
            db_conn.session.rollback()
            raise Exception
        except ModuleNotFoundError:
            db_conn.session.close()
            raise ModuleNotFoundError
        finally:
            db_conn.session.close()
