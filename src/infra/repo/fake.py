from src.infra.config import DbConnectionHandler
from src.infra.entities import Users


class FakerRepository:
    """ Simple fake repository """

    @classmethod
    def insert_user(cls):
        """ Method to add a user in DB """

        with DbConnectionHandler() as db_conn:
            try:
                new_user = Users(name=str(input('Nome: ')), password=str(input('Senha: ')))
                db_conn.session.add(new_user)
                db_conn.session.commit()
            except:
                db_conn.session.rollback()
            finally:
                db_conn.session.close()
