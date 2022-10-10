def test_insert_pet(petrepo, petname, specie, age, user_id, engine):
    new_pet = petrepo.insert_pet(petname=petname, specie=specie, age=age, user_id=user_id)
    query_pet = engine.execute(f"SELECT * FROM pets WHERE id='{new_pet.id}';").fetchone()
    engine.execute(f"DELETE FROM pets WHERE id='{new_pet.id}';")
    # Assertions
    assert query_pet.id == new_pet.id
    assert query_pet.petname == new_pet.petname
    assert query_pet.specie == new_pet.specie
    assert query_pet.age == new_pet.age
    assert query_pet.user_id == new_pet.user_id
    assert query_pet.register_date is not None
