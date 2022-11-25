from .find_pet_composite import find_pet_composer
from src.presenters.controllers import FindPetController


def test_find_pet_composite():
    response = find_pet_composer()
    assert FindPetController.__name__ == type(response).__name__
