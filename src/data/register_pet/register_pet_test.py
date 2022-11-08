from src.data.register_pet import RegisterPet
from src.infra.errors import NoResultFoundError


def test_register_pet(pet_repo, user_repo, petname, specie, age, user_id):
    user_repo.id = user_id
    register = RegisterPet(user_repository=user_repo, pet_repository=pet_repo)
    pet = register.register(petname=petname, specie=specie, age=age, user_id=user_id)
    assert pet["success"]
    assert pet['data'].petname == petname
    assert pet['data'].age == age
    assert pet['data'].specie == specie
    assert pet['data'].user_id == user_id


def test_register_pet_no_result_found_error(pet_repo, user_repo, petname, specie, age, user_id):
    user_repo.id = user_id + 1
    register = RegisterPet(user_repository=user_repo, pet_repository=pet_repo)
    pet = register.register(petname=petname, specie=specie, age=age, user_id=user_id)
    # Assertion expect to raise NoResultFound error
    assert type(pet['detail']).__name__ == NoResultFoundError.__name__
    assert not pet["success"]
