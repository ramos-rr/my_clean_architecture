import pytest
import src.data.register_pet.conftest
from src.infra.config import CreateDataBase
from src.infra.errors import InsufficientDataError, NoResultFoundError
from src.infra.errors.pets_errors import PetNameTypeError, PetNameNotProvidedError, SpecieNotProvidedError, \
    SpecieNotAllowedError, SpecieTypeError, AgeNotIntegerError, PetIdNotIntegerError, AgeNotProvidedError
from src.infra.errors.users_errors.user_id_error import UserIdNotProvidedError, UserIdNotIntegerError


# Check for DB path. If it doesn't exist, system will create one with tables
CreateDataBase.create_db()


def test_insert_pet(petrepo, petname, specie, age, user_id, engine):
    new_pet = petrepo.insert_pet(petname=petname, specie=specie, age=age, user_id=user_id)
    query_pet = engine.execute(f"SELECT * FROM pets WHERE id='{new_pet.id}';").fetchone()
    engine.execute(f"DELETE FROM pets WHERE id='{new_pet.id}';")
    # Assertions
    assert query_pet.id == new_pet.id
    assert query_pet.petname == new_pet.petname
    assert src.data.register_pet.conftest.specie == src.data.register_pet.conftest.specie
    assert query_pet.age == new_pet.age
    assert query_pet.user_id == new_pet.user_id
    assert query_pet.register_date is not None


def test_insert_pet_name_not_provided_error(petrepo, specie, age, user_id):
    with pytest.raises(PetNameNotProvidedError):
        new_pet = petrepo.insert_pet(petname=None, specie=specie, age=age, user_id=user_id)
        return new_pet


def test_insert_pet_name_type_error(petrepo, specie, age, user_id):
    with pytest.raises(PetNameTypeError):
        new_pet = petrepo.insert_pet(petname=1234, specie=specie, age=age, user_id=user_id)
        return new_pet


def test_insert_pet_specie_not_provided_error(petrepo, petname, age, user_id):
    with pytest.raises(SpecieNotProvidedError):
        new_pet = petrepo.insert_pet(petname=petname, specie=None, age=age, user_id=user_id)
        return new_pet


def test_insert_pet_specie_not_allowed_error(petrepo, petname, age, user_id):
    with pytest.raises(SpecieNotAllowedError):
        new_pet = petrepo.insert_pet(petname=petname, specie='bug', age=age, user_id=user_id)
        return new_pet


def test_insert_pet_specie_type_error(petrepo, petname, age, user_id):
    with pytest.raises(SpecieTypeError):
        new_pet = petrepo.insert_pet(petname=petname, specie=1234, age=age, user_id=user_id)
        return new_pet


def test_insert_pet_age_not_integer_error(petrepo, petname, specie, user_id):
    with pytest.raises(AgeNotIntegerError):
        new_pet = petrepo.insert_pet(petname=petname, specie=specie, age='abc', user_id=user_id)
        return new_pet


def test_insert_pet_age_not_provided_error(petrepo, petname, specie, user_id):
    with pytest.raises(AgeNotProvidedError):
        new_pet = petrepo.insert_pet(petname=petname, specie=specie, age=None, user_id=user_id)
        return new_pet


def test_insert_pet_age_user_id_not_integer_error(petrepo, petname, specie, age):
    with pytest.raises(UserIdNotIntegerError):
        new_pet = petrepo.insert_pet(petname=petname, specie=specie, age=age, user_id='abc')
        return new_pet


def test_insert_pet_age_user_id_not_provided_error(petrepo, petname, specie, age):
    with pytest.raises(UserIdNotProvidedError):
        new_pet = petrepo.insert_pet(petname=petname, specie=specie, age=age, user_id=None)
        return new_pet


# TESTS FOR SELECT_PET
def test_select_pet(petrepo, pet_id, petname, specie, age, user_id, engine):
    from src.infra.entities import Pets as PetEntity
    # insert first pet
    data1 = PetEntity(id=pet_id, petname=petname, specie=specie, age=age, user_id=user_id)
    engine.execute(
        f"INSERT INTO pets (id, petname, specie, age, user_id) VALUES "
        f"('{pet_id}', '{petname}', '{specie}', '{age}', '{user_id}');")
    # insert second pet
    data2 = PetEntity(id=pet_id + 1, petname=petname + 's', specie=specie, age=age + 1, user_id=user_id)
    engine.execute(
        f"INSERT INTO pets (id, petname, specie, age, user_id) VALUES "
        f"('{pet_id + 1}', '{petname}s', '{specie}', '{age + 1}', '{user_id}');")
    query_pet1 = petrepo.select_pet(pet_id=pet_id)
    query_pet2 = petrepo.select_pet(user_id=user_id)
    query_pet3 = petrepo.select_pet(pet_id=pet_id, user_id=user_id)
    engine.execute(f"DELETE FROM pets WHERE user_id='{user_id}';")
    assert data1 in query_pet1
    assert data1 in query_pet2
    assert data2 in query_pet2
    assert data1 in query_pet3


def test_select_pet_insufficient_data_error(petrepo):
    with pytest.raises(InsufficientDataError):
        petrepo.select_pet()


def test_select_pet_name_type_error(petrepo):
    with pytest.raises(PetIdNotIntegerError):
        petrepo.select_pet(pet_id='abc')


def test_select_pet_id_not_integer_error(petrepo):
    with pytest.raises(UserIdNotIntegerError):
        petrepo.select_pet(user_id='abc')


def test_select_pet_by_pet_id_no_result_found_error(petrepo):
    with pytest.raises(NoResultFoundError):
        petrepo.select_pet(pet_id=999999)


def test_select_pet_by_user_id_no_result_found_error(petrepo):
    with pytest.raises(NoResultFoundError):
        petrepo.select_pet(user_id=999999)


def test_select_pet_by_pet_id_and_user_id_no_result_found_error(petrepo):
    with pytest.raises(NoResultFoundError):
        petrepo.select_pet(pet_id=999999, user_id=999999)
