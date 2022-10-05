def test_insert_user(repo, name, password, engine):
    # SQL Command
    new_user = repo.insert_user(name=name, password=password)
    query_user = engine.execute("SELECT * FROM users WHERE id='{}';".format(new_user.id)).fetchone()
    # DELETE TEST INSERTION
    engine.execute(f"DELETE FROM users WHERE id='{query_user.id}'")
    # Assertions
    assert new_user.id == query_user.id
    assert new_user.name == query_user.name
    assert new_user.password == query_user.password


def test_select_user(name, password, engine, user_id, repo):
    from src.infra.entities.users import Users as UsersEntity
    """ Should select a user in Users table and compare it"""
    data = UsersEntity(id=user_id, name=name, password=password)
    engine.execute(
        f"INSERT INTO users (id, name, password) VALUES ('{user_id}','{name}','{password}');")
    query_user1 = repo.select_user(user_id=user_id)
    query_user2 = repo.select_user(name=name)
    query_user3 = repo.select_user(user_id=user_id, name=name)

    assert data in query_user1
    assert data in query_user2
    assert data in query_user3

    engine.execute(f"DELETE FROM users WHERE id='{user_id}'")
