import pytest
import inject
import bcrypt
from User import User, user_factory


def test_user_factory():
    name = "Marco Tulio"
    username = "marco"
    password: bytes = "senha".encode()
    password_salt: bytes = bcrypt.gensalt()
    password_hash: bytes = bcrypt.hashpw(password, password_salt)

    user = user_factory(name, username, password_hash, password_salt)

    try_password_hash = bcrypt.hashpw("senha".encode(), user.password_salt.encode())

    assert user.followers_counter == 0
    assert user.following_counter == 0
    assert user.name == "Marco Tulio"
    assert user.username == "marco"
    assert try_password_hash.decode() == user.password_hash