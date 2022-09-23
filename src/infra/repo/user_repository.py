from src.infra.config import DbConnectionHandler
from src.infra.entities import Users


class UserRepository:
    """ Class to manage Users """

    @classmethod
    def insert_user(cls, name: str, password: str):
        """
        Method to insert new user
        """
        with DbConnectionHandler() as db_conn:
            try:
                new_user = Users(name=name, password=password)
                db_conn.session.add(new_user)
                db_conn.session.commit()
            except:
                db_conn.session.rollback()
            finally:
                db_conn.session.close()
