from RoadmapService import RoadmapService
from FollowService import FollowService
from UserService import UserService
import inject
import bcrypt
import pytest
from adapters.db.InMemoryUserRepository import InMemoryUserRepository
from adapters.db.InMemoryRoadmapRepository import InMemoryRoadmapRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository

from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.AlreadyDislikedException import AlreadyDislikedException
from domain.exceptions.NotLikedException import NotLikedException
from domain.exceptions.NotDislikedException import NotDislikedException
from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException


@pytest.fixture()
def setup():
    repositorio_user = InMemoryUserRepository()
    user_service = UserService(repositorio_user)
    repositorio_follow = InMemoryFollowRepository(repositorio_user)
    follow_service = FollowService(repositorio_follow, repositorio_user)
    repositorio_roadmap = InMemoryRoadmapRepository(repositorio_follow)
    roadmap_service = RoadmapService(repositorio_roadmap, repositorio_user)
    yield roadmap_service, follow_service, user_service

def test_roadmap_create_successfully(setup):
    roadmap_service, follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    assert roadmap.author_username == "marco"
    assert roadmap.title == "titulo"
    assert roadmap.description == "desc"
    assert roadmap.coordinates[0][0] == 0
    assert roadmap.coordinates[0][1] == 0
    assert roadmap.tags[0] == "tag1"
    assert roadmap.likes == 0
    assert roadmap.dislikes == 0

def test_roadmap_create_missing(setup):
    roadmap_service, follow_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        roadmap_service.create(None, "titulo", "desc", [[0, 0]], ["tag1"])
    
    with pytest.raises(MissingFieldException):
        roadmap_service.create(user.username, None, "desc", [[0, 0]], ["tag1"])
    
    with pytest.raises(MissingFieldException):
        roadmap_service.create(user.username, "titulo", None, [[0, 0]], ["tag1"])
    
    with pytest.raises(MissingFieldException):
        roadmap_service.create(user.username, "titulo", "desc", None, ["tag1"])
    
    with pytest.raises(MissingFieldException):
        roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], None)

def test_roadmap_create_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        roadmap_service.create("marquinhos", "titulo", "desc", [[0, 0]], ["tag1"])

def test_roadmap_find_all(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmaps = roadmap_service.find_all()
    roadmap2 = roadmaps[0]

    assert len(roadmaps) == 1
    assert roadmap.author_username == roadmap2.author_username
    assert roadmap.title == roadmap2.title
    assert roadmap.description == roadmap2.description
    assert roadmap.coordinates[0][0] == roadmap2.coordinates[0][0]
    assert roadmap.coordinates[0][1] == roadmap2.coordinates[0][1]
    assert roadmap.tags[0] == roadmap2.tags[0]
    assert roadmap.likes == roadmap2.likes
    assert roadmap.dislikes == roadmap2.dislikes

def test_roadmap_find_by_id(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_id = roadmap_service.find_all()[0].id

    roadmap2 = roadmap_service.find_by_id(roadmap_id)

    assert roadmap.author_username == roadmap2.author_username
    assert roadmap.title == roadmap2.title
    assert roadmap.description == roadmap2.description
    assert roadmap.coordinates[0][0] == roadmap2.coordinates[0][0]
    assert roadmap.coordinates[0][1] == roadmap2.coordinates[0][1]
    assert roadmap.tags[0] == roadmap2.tags[0]
    assert roadmap.likes == roadmap2.likes
    assert roadmap.dislikes == roadmap2.dislikes

def test_roadmap_find_by_id_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.find_by_id(None)

def test_roadmap_find_by_id_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        roadmap_service.find_by_id("not_valid_id")

def test_roadmap_find_by_username(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap2 = roadmap_service.find_all_by_username("marco")[0]

    assert roadmap.author_username == roadmap2.author_username
    assert roadmap.title == roadmap2.title
    assert roadmap.description == roadmap2.description
    assert roadmap.coordinates[0][0] == roadmap2.coordinates[0][0]
    assert roadmap.coordinates[0][1] == roadmap2.coordinates[0][1]
    assert roadmap.tags[0] == roadmap2.tags[0]
    assert roadmap.likes == roadmap2.likes
    assert roadmap.dislikes == roadmap2.dislikes

def test_roadmap_find_all_by_username_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.find_all_by_username(None)

def test_roadmap_find_all_by_username_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        roadmap_service.find_all_by_username("not_valid_id")

def test_roadmap_find_by_following(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")
    user2 = user_service.create(name="Tulio", username="tulio", password="123456")

    follow_service.follow(user.username, user2.username)

    roadmap = roadmap_service.create(user2.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap2 = roadmap_service.find_all_by_following("marco")[0]

    assert roadmap.author_username == roadmap2.author_username
    assert roadmap.title == roadmap2.title
    assert roadmap.description == roadmap2.description
    assert roadmap.coordinates[0][0] == roadmap2.coordinates[0][0]
    assert roadmap.coordinates[0][1] == roadmap2.coordinates[0][1]
    assert roadmap.tags[0] == roadmap2.tags[0]
    assert roadmap.likes == roadmap2.likes
    assert roadmap.dislikes == roadmap2.dislikes

def test_roadmap_find_all_by_following_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.find_all_by_following(None)

def test_roadmap_find_all_by_following_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(NotFoundException):
        roadmap_service.find_all_by_following("not_valid_user")


def test_roadmap_find_all_by_tags(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap2 = roadmap_service.find_all_by_tags(["tag1"])[0]

    assert roadmap.author_username == roadmap2.author_username
    assert roadmap.title == roadmap2.title
    assert roadmap.description == roadmap2.description
    assert roadmap.coordinates[0][0] == roadmap2.coordinates[0][0]
    assert roadmap.coordinates[0][1] == roadmap2.coordinates[0][1]
    assert roadmap.tags[0] == roadmap2.tags[0]
    assert roadmap.likes == roadmap2.likes
    assert roadmap.dislikes == roadmap2.dislikes

def test_roadmap_find_all_by_tags_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.find_all_by_tags(None)


def test_roadmap_is_liked_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.is_liked(None, None)
    
    with pytest.raises(MissingFieldException):
        roadmap_service.is_liked("user", None)

    with pytest.raises(MissingFieldException):
        roadmap_service.is_liked(None, "1")

def test_roadmap_is_liked_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(NotFoundException):
        roadmap_service.is_liked("user", "1")

    with pytest.raises(NotFoundException):
        roadmap_service.is_liked("marco", "1")

def test_roadmap_is_liked_successfully(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    assert roadmap_service.is_liked(user.username, roadmap.id) == False

    roadmap_service.add_like(user.username, roadmap.id)

    assert roadmap_service.is_liked(user.username, roadmap.id) == True

def test_roadmap_add_like_missing(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        roadmap_service.add_like(None, None)
    
    with pytest.raises(MissingFieldException):
        roadmap_service.add_like(user.username, None)

    with pytest.raises(MissingFieldException):
        roadmap_service.add_like(None, roadmap.id)

def test_roadmap_add_like_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotFoundException):
        roadmap_service.add_like("not_found", "not_found")
    
    with pytest.raises(NotFoundException):
        roadmap_service.add_like(user.username, "not_found")

    with pytest.raises(NotFoundException):
        roadmap_service.add_like("not_found", roadmap.id)

def test_roadmap_add_like_already_liked(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_like(user.username, roadmap.id)

    with pytest.raises(AlreadyLikedException):
        roadmap_service.add_like(user.username, roadmap.id)


def test_roadmap_is_disliked_missing(setup):
    roadmap_service, follow_service, user_service = setup

    with pytest.raises(MissingFieldException):
        roadmap_service.is_disliked(None, None)
    
    with pytest.raises(MissingFieldException):
        roadmap_service.is_disliked("user", None)

    with pytest.raises(MissingFieldException):
        roadmap_service.is_disliked(None, "1")

def test_roadmap_is_disliked_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    with pytest.raises(NotFoundException):
        roadmap_service.is_disliked("user", "1")

    with pytest.raises(NotFoundException):
        roadmap_service.is_disliked("marco", "1")

def test_roadmap_is_disliked_successfully(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    assert roadmap_service.is_disliked(user.username, roadmap.id) == False

    roadmap_service.add_dislike(user.username, roadmap.id)

    assert roadmap_service.is_disliked(user.username, roadmap.id) == True

def test_roadmap_add_dislike_missing(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        roadmap_service.add_dislike(None, None)
    
    with pytest.raises(MissingFieldException):
        roadmap_service.add_dislike(user.username, None)

    with pytest.raises(MissingFieldException):
        roadmap_service.add_dislike(None, roadmap.id)

def test_roadmap_add_dislike_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotFoundException):
        roadmap_service.add_dislike("not_found", "not_found")
    
    with pytest.raises(NotFoundException):
        roadmap_service.add_dislike(user.username, "not_found")

    with pytest.raises(NotFoundException):
        roadmap_service.add_dislike("not_found", roadmap.id)

def test_roadmap_add_dislike_already_liked(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_dislike(user.username, roadmap.id)

    with pytest.raises(AlreadyDislikedException):
        roadmap_service.add_dislike(user.username, roadmap.id)

def test_roadmap_remove_like_missing(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_like(user.username, roadmap.id)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_like(None, None)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_like(None, roadmap.id)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_like(user.username, None)

def test_roadmap_remove_dislike_missing(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_dislike(user.username, roadmap.id)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_dislike(None, None)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_dislike(None, roadmap.id)

    with pytest.raises(MissingFieldException):
        roadmap_service.remove_dislike(user.username, None)

def test_roadmap_remove_like_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_like(user.username, roadmap.id)

    with pytest.raises(NotFoundException):
        roadmap_service.remove_like("not_found", "not_found")

    with pytest.raises(NotFoundException):
        roadmap_service.remove_like("not_found", roadmap.id)

    with pytest.raises(NotFoundException):
        roadmap_service.remove_like(user.username, "not_found")

def test_roadmap_remove_dislike_not_found(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_dislike(user.username, roadmap.id)

    with pytest.raises(NotFoundException):
        roadmap_service.remove_dislike("not_found", "not_found")

    with pytest.raises(NotFoundException):
        roadmap_service.remove_dislike("not_found", roadmap.id)

    with pytest.raises(NotFoundException):
        roadmap_service.remove_dislike(user.username, "not_found")

def test_roadmap_remove_like_not_liked(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotLikedException):
        roadmap_service.remove_like(user.username, roadmap.id)

def test_roadmap_remove_dislike_not_disliked(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotDislikedException):
        roadmap_service.remove_dislike(user.username, roadmap.id)

def test_roadmap_remove_like_successfully(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_like(user.username, roadmap.id)

    assert roadmap.likes == 1

    roadmap_service.remove_like(user.username, roadmap.id)

    assert roadmap.likes == 0

def test_roadmap_remove_dislike_successfully(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_dislike(user.username, roadmap.id)

    assert roadmap.dislikes == 1

    roadmap_service.remove_dislike(user.username, roadmap.id)

    assert roadmap.dislikes == 0

def test_roadmap_like_and_dislike(setup):
    roadmap_service, follow_service, user_service = setup

    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    roadmap_service.add_like(user.username, roadmap.id)
    roadmap_service.add_dislike(user.username, roadmap.id)
    roadmap_service.add_like(user.username, roadmap.id)
    roadmap_service.add_dislike(user.username, roadmap.id)

    assert roadmap.dislikes == 1

    roadmap_service.remove_dislike(user.username, roadmap.id)

    assert roadmap.dislikes == 0