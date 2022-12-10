from UserService import UserService
import inject
import bcrypt
import pytest
from adapters.db.InMemoryUserRepository import InMemoryUserRepository

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.UsernameAlreadyExistsException import UsernameAlreadyExistsException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException

from domain.ports.IUserService import IUserService
from domain.ports.IUserRepository import IUserRepository

from domain.models.User import User, user_factory


@pytest.fixture()
def setup():
    repositorio = InMemoryUserRepository()
    user_service = UserService(repositorio)
    yield user_service


def test_user_service_create_successfully(setup):
    user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    assert user.name == "Marco"
    assert user.username == "marco"

def test_user_service_create_without_username(setup):
    user_service = setup
    with pytest.raises(MissingFieldException):
        user = user_service.create(name="Marco", username=None, password="123456")

def test_user_service_create_already_exists(setup):
    user_service = setup
    with pytest.raises(UsernameAlreadyExistsException):
        name = "Marco"
        username = "marco"
        password="123456"

        user = user_service.create(name, username, password)
        user2 = user_service.create(name, username, password)

def test_user_service_is_password_correct(setup):
    user_service = setup

    name = "Marco"
    username = "marco"
    password="123456"

    user = user_service.create(name, username, password)

    assert user_service.is_password_correct(user, password) == True
    assert user_service.is_password_correct(user, "1234567") == False

def test_user_service_login_successfully(setup):
    user_service = setup

    name = "Marco"
    username = "marco"
    password="123456"

    user = user_service.create(name, username, password)

    user2 = user_service.login(username, password)

    assert user.name == user2.name 
    assert user.username == user2.username 

def test_user_service_login_missing_field(setup):
    with pytest.raises(MissingFieldException):
        user_service = setup

        name = "Marco"
        username = "marco"
        password="123456"

        user = user_service.create(name, username, password)
        user2 = user_service.login(None, password)

def test_user_service_login_password_incorrect(setup):
    with pytest.raises(UnauthorizedException):
        user_service = setup

        name = "Marco"
        username = "marco"
        password="123456"
        password2="1234567"

        user = user_service.create(name, username, password)
        user2 = user_service.login(username, password2)

def test_user_service_find_all_2_users(setup):
    user_service = setup

    name = "Marco"
    username = "marco"
    username2 = "marco2"
    password="123456"

    user_service.create(name, username, password)
    user_service.create(name, username2, password)
    users = user_service.find_all()

    assert len(users) == 2
    assert users[0].username == "marco"
    assert users[1].username == "marco2"

def test_user_service_find_all_empty(setup):
    user_service = setup

    users = user_service.find_all()

    assert len(users) == 0

def test_user_service_find_by_username_successfully(setup):
    user_service = setup

    name = "Marcos"
    username = "marcos"
    password="123456"

    user = user_service.create(name, username, password)

    user2 = user_service.find_by_username(username)

    assert user.name == user2.name 
    assert user.username == user2.username 

def test_user_service_find_by_username_missing_field(setup):
    with pytest.raises(MissingFieldException):
        user_service = setup

        user = user_service.find_by_username(None)

def test_user_service_find_by_username_not_found(setup):
    with pytest.raises(NotFoundException):
        user_service = setup

        username = "marquinhos"

        user = user_service.find_by_username(username)