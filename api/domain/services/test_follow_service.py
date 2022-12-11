from FollowService import FollowService
from UserService import UserService
import inject
import bcrypt
import pytest
from adapters.db.InMemoryUserRepository import InMemoryUserRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.SameUserException import SameUserException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.AlreadyFollowException import AlreadyFollowException
from domain.exceptions.NotFollowerException import NotFollowerException

@pytest.fixture()
def setup():
    repositorio_user = InMemoryUserRepository()
    user_service = UserService(repositorio_user)
    repositorio_follow = InMemoryFollowRepository(repositorio_user)
    follow_service = FollowService(repositorio_follow, repositorio_user)
    yield follow_service, user_service

def test_follow_follow(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    assert follow_service.follow(user.username, user2.username) == True
    assert user.following_counter == 1
    assert user2.following_counter == 0
    assert user.followers_counter == 0
    assert user2.followers_counter == 1

def test_follow_follow_missing(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(MissingFieldException):
        follow_service.follow(None, user.username)

    with pytest.raises(MissingFieldException):
        follow_service.follow(user.username, None)


def test_follow_follow_same_user(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(SameUserException):
        follow_service.follow(user.username, user.username)

def test_follow_follow_not_found(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(NotFoundException):
        follow_service.follow(user.username, "tulio")
    
    with pytest.raises(NotFoundException):
        follow_service.follow("tulio", user.username)

def test_follow_follow_already_follow(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    follow_service.follow(user.username, user2.username)

    with pytest.raises(AlreadyFollowException):
        follow_service.follow(user.username, user2.username)

def test_follow_is_follower(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    follow_service.follow(user.username, user2.username)

    assert follow_service.is_follower(user.username, user2.username) == True

def test_follow_is_follower_missing(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(MissingFieldException):
        follow_service.is_follower(None, user.username)
    
    with pytest.raises(MissingFieldException):
        follow_service.is_follower(user.username, None)
    

def test_follow_is_follower_not_found(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(NotFoundException):
        follow_service.is_follower(user.username, "tulio")
    
    with pytest.raises(NotFoundException):
        follow_service.is_follower("tulio", user.username)

def test_follow_is_follower_same_user(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(SameUserException):
        follow_service.is_follower(user.username, user.username)




def test_follow_unfollow(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    follow_service.follow(user.username, user2.username)

    assert follow_service.unfollow(user.username, user2.username) == True
    assert user.following_counter == 0
    assert user2.following_counter == 0
    assert user.followers_counter == 0
    assert user2.followers_counter == 0

def test_follow_unfollow_missing(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(MissingFieldException):
        follow_service.unfollow(None, user.username)

    with pytest.raises(MissingFieldException):
        follow_service.unfollow(user.username, None)


def test_follow_unfollow_same_user(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(SameUserException):
        follow_service.unfollow(user.username, user.username)

def test_follow_unfollow_not_found(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(NotFoundException):
        follow_service.unfollow(user.username, "tulio")
    
    with pytest.raises(NotFoundException):
        follow_service.unfollow("tulio", user.username)

def test_follow_unfollow_not_follower(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    with pytest.raises(NotFollowerException):
        follow_service.unfollow(user.username, user2.username)
    with pytest.raises(NotFollowerException):
        follow_service.unfollow(user2.username, user.username)

def test_follow_find_all_followers_missing(setup):
    follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        follow_service.find_all_followers(None)

def test_follow_find_all_followers_not_found(setup):
    follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        follow_service.find_all_followers("marco")

def test_follow_find_all_followers(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    user3 = user_service.create(name="Valente", username="valente", password="345678")

    follow_service.follow(user2.username, user.username)
    follow_service.follow(user3.username, user.username)

    assert len(follow_service.find_all_followers(user.username)) == 2
    assert follow_service.find_all_followers(user.username)[0].username == "tulio"
    assert follow_service.find_all_followers(user.username)[1].username == "valente"


def test_follow_find_all_following_missing(setup):
    follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        follow_service.find_all_following(None)

def test_follow_find_all_following_not_found(setup):
    follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        follow_service.find_all_following("marco")

def test_follow_find_all_following(setup):
    follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    user2 = user_service.create(name="Tulio", username="tulio", password="234567")

    user3 = user_service.create(name="Valente", username="valente", password="345678")

    follow_service.follow(user.username, user2.username)
    follow_service.follow(user.username, user3.username)

    assert len(follow_service.find_all_following(user.username)) == 2
    assert follow_service.find_all_following(user.username)[0].username == "tulio"
    assert follow_service.find_all_following(user.username)[1].username == "valente"