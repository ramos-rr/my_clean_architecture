from .users import Users


def test_users():
    user = Users()
    assert user.id is None
    assert user.username is None
    assert user.password is None
    assert user.register_date is None
