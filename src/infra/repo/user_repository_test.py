import pytest
# import datetime
# from src.infra.entities import Users
# from faker import Faker
#
# faker = Faker()
from src.infra.errors import UserNameNotProvidedError, UserNameTypeError, PasswordNotProvidedError, \
    PasswordWithoutLettersError, PasswordWithoutNumbersError, PasswordTypeError, InsufficientDataError, \
    UserIdNotIntegerError, NoResultFoundError, IntegrityError
from src.infra.config import CreateDataBase

# Check for DB path. If it doesn't exist, system will create one with tables
CreateDataBase.create_db()


# TESTS FOR INSERT USER
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


def test_insert_user_duplicate_username_error(userrepo, username, password, engine):
    with pytest.raises(IntegrityError):
        engine.execute(f"INSERT INTO users (username, password) VALUES ('{username}','{password}');")
        try:
            _ = userrepo.insert_user(username=username, password=password)
        finally:
            engine.execute(f"DELETE FROM users WHERE username='{username}'")


def test_inset_user_name_not_provided_error(userrepo, password):
    with pytest.raises(UserNameNotProvidedError):
        new_user = userrepo.insert_user(username=None, password=password)
        return new_user


def test_inset_user_name_type_error(userrepo, password):
    with pytest.raises(UserNameTypeError):
        new_user = userrepo.insert_user(username=134, password=password)
        return new_user


def test_inset_user_password_not_provided_error(userrepo, username):
    with pytest.raises(PasswordNotProvidedError):
        _ = userrepo.insert_user(username=username, password=None)


def test_inset_user_password_without_letters_error(userrepo, username):
    with pytest.raises(PasswordWithoutLettersError):
        _ = userrepo.insert_user(username=username, password='1234')


def test_inset_user_password_type_error(userrepo, username):
    with pytest.raises(PasswordTypeError):
        _ = userrepo.insert_user(username=username, password=1234)


def test_inset_user_password_without_numbers_error(userrepo, username):
    with pytest.raises(PasswordWithoutNumbersError):
        _ = userrepo.insert_user(username=username, password='abcd')

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


# TESTS FOR SELECT USER
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


def test_select_user_insufficient_data_error(userrepo):
    with pytest.raises(InsufficientDataError):
        userrepo.select_user()


def test_select_user_name_type_error(userrepo):
    with pytest.raises(UserNameTypeError):
        userrepo.select_user(username=123)


def test_select_user_id_not_integer_error(userrepo):
    with pytest.raises(UserIdNotIntegerError):
        userrepo.select_user(user_id='abc')


def test_select_user_no_result_found_error(userrepo):
    with pytest.raises(NoResultFoundError):
        userrepo.select_user(user_id=999999)
