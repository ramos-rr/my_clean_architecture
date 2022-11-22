from .register_user_composite import register_user_composer
from src.presenters.controllers import RegisterUserController


def test_register_user_composer():
    response = register_user_composer()
    assert type(response).__name__ == RegisterUserController.__name__
