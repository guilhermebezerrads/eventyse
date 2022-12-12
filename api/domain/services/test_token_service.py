import pytest
import os, datetime
from adapters.db.InMemoryUserRepository import InMemoryUserRepository
from TokenService import TokenService
from UserService import UserService
from unittest import mock
from domain.exceptions.TokenException import TokenException
from domain.models.User import User, user_factory
import bcrypt

@pytest.fixture(autouse=True)
def mock_env():
    with mock.patch.dict(os.environ, {"SECRET_KEY": "bolodecenoura"}):
        yield

@pytest.fixture()
def setup():
    repositorio = InMemoryUserRepository()
    token_service = TokenService(repositorio)
    user_service = UserService(repositorio)
    yield token_service, user_service


def test_token_service_create_token(setup):
    token_service, user_service = setup

    user = user_service.create("Marco", "marco", "123456")

    token = token_service.create_token(user)

    assert type(token) == str


def test_token_service_authenticate_token_successfully(setup):
    token_service, user_service = setup

    user = user_service.create("Marco", "marco", "123456")

    token = token_service.create_token(user)

    user2 = token_service.authenticate_token(token)

    assert user.username == user2.username

def test_token_service_authenticate_token_missing(setup):
    with pytest.raises(TokenException):
        token_service, user_service = setup

        user = token_service.authenticate_token(None)

def test_token_service_authenticate_token_invalid(setup):
    with pytest.raises(TokenException):
        token_service, user_service = setup

        name = "Marco Tulio"
        username = "marco"
        password_salt: bytes = bytes(123)
        password_hash: bytes = bytes(123)

        user = user_factory(name, username, password_hash, password_salt)

        token = token_service.create_token(user)
        user2 = token_service.authenticate_token(token)

def test_token_service_authenticate_token_expired(setup):
    token_service, user_service = setup

    user = user_service.create("Marco", "marco", "123456")

    token = token_service.create_token(user, datetime.datetime.now() - datetime.timedelta(hours=24))

    with pytest.raises(TokenException):
        user2 = token_service.authenticate_token(token)