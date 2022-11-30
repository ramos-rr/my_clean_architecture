# Configuration to run.py
# Objective is to verify whether there's an active Database in place and if there's at list one Superuser to use the app
from src.infra.entities import Users
from src.infra.config import CreateDataBase, DbConnectionHandler


def set_up_before_run():

    CreateDataBase.create_db()
    conn = DbConnectionHandler()
    conn.__enter__()
    query = None
    try:
        query = conn.session.query(Users).filter_by(superuser=True).all()
    except Exception as error:
        print(error.args)
    else:
        if query is None or len(query) == 0:
            print('\033[31;1mNo superuser has been found.\033[m\n'
                  'Only superusers can access routes from browsers. \033[1mWould you like to create one?\033[m')
            resp = input(str("[ Y / N ]: ")).strip().lower()[0]
            if resp in 'yY':
                while True:
                    inputusername = input(str("Username (must not have spaces): "))
                    inputpassword = input(str("Password (must have letters and numbers, but no spaces): "))
                    try:
                        new = Users(username=inputusername, password=inputpassword, superuser=True)
                        conn.session.add(new)
                        conn.session.commit()
                    except Exception as error:
                        conn.session.rollback()
                        print(error.args)
                        continue
                    else:
                        print(f'Superuser registered: {new.username} - {new.password}')
                        conn.session.close()
                        break
            else:
                print('Launching server without superuser')
                conn.session.close()

        elif len(query) == 1:
            print(f'There is {len(query)} Superuser:')
            print(f'> {query[0].username} - {query[0].password}')
            conn.session.close()

        elif len(query) > 1:
            print(f'There are {len(query)} Superusers:')
            for user in query:
                print(f'> {user.username} - {user.password}')
            conn.session.close()
