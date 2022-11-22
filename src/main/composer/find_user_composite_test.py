from .find_user_composite import find_user_composer
from src.presenters.controllers import FindUserController


def test_find_user_composite():
    response = find_user_composer()
    assert FindUserController.__name__ == type(response).__name__
