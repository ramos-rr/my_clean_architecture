from .register_pet_composite import register_pet_composer
from src.presenters.controllers import RegisterPetController


def test_register_pet_composer():
    response = register_pet_composer()
    assert type(response).__name__ == RegisterPetController.__name__
