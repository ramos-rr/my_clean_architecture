# import pytest
# import datetime
# from src.infra.entities import Users
# from faker import Faker
#
# faker = Faker()


def test_insert_user(userrepo, username, password, engine):
    # SQL Command
    new_user = userrepo.insert_user(username=username, password=password)
    query_user = engine.execute("SELECT * FROM users WHERE id='{}';".format(new_user.id)).fetchone()
    # DELETE TEST INSERTION
    engine.execute(f"DELETE FROM users WHERE id='{query_user.id}'")
    # Assertions
    assert new_user.id == query_user.id
    assert new_user.username == query_user.username
    assert new_user.password == query_user.password


# @pytest.mark.parametrize(
#     'user_list', [
#         Users(username=faker.name(), password=f'{faker.random_number(digits=5)}'),
#         Users(username=faker.name(), password=f'{faker.random_number(digits=5)}'),
#         Users(username=faker.name(), password=f'{faker.random_number(digits=5)}'),
#     ]
# )
# def test_insert_user_register_time_is_different(userrepo, engine, user_list, db_conn):
#     db_conn.session.add(user_list)
#     db_conn.session.commit()


def test_select_user(username, password, engine, user_id, userrepo):
    from src.infra.entities.users import Users as UsersEntity
    """ Should select a user in Users table and compare it"""
    data = UsersEntity(id=user_id, username=username, password=password)
    engine.execute(
        f"INSERT INTO users (id, username, password) VALUES ('{user_id}','{username}','{password}');")
    query_user1 = userrepo.select_user(user_id=user_id)
    query_user2 = userrepo.select_user(username=username)
    query_user3 = userrepo.select_user(user_id=user_id, username=username)

    assert data in query_user1
    assert data in query_user2
    assert data in query_user3

    engine.execute(f"DELETE FROM users WHERE id='{user_id}'")
