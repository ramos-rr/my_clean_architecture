def test_insert_user(repo, name, password, engine, db_conn):
    # SQL Command
    new_user = repo.insert_user(name=name, password=password, database=db_conn)
    print(new_user)
    query_user = engine.execute("SELECT * FROM users WHERE id='{}';".format(new_user.id)).fetchone()
    print(query_user)
    # DELETE TEST INSERTION
    engine.execute(f"DELETE FROM users WHERE id='{query_user.id}'")
    # Assertions
    assert new_user.id == query_user.id
    assert new_user.name == query_user.name
    assert new_user.password == query_user.password
