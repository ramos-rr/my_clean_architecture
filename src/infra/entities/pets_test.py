from .pets import Pets


def test_pets():
    pet = Pets()
    assert pet.id is None
    assert pet.petname is None
    assert pet.specie is None
    assert pet.age is None
    assert pet.user_id is None
    assert pet.register_date is None
