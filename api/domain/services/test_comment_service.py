from RoadmapService import RoadmapService
from FollowService import FollowService
from UserService import UserService
from CommentService import CommentService
import inject
import bcrypt
import pytest
from adapters.db.InMemoryUserRepository import InMemoryUserRepository
from adapters.db.InMemoryRoadmapRepository import InMemoryRoadmapRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository

from adapters.db.InMemoryCommentRepository import InMemoryCommentRepository

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException

@pytest.fixture()
def setup():
    repositorio_user = InMemoryUserRepository()
    user_service = UserService(repositorio_user)
    repositorio_follow = InMemoryFollowRepository(repositorio_user)
    repositorio_roadmap = InMemoryRoadmapRepository(repositorio_follow)
    roadmap_service = RoadmapService(repositorio_roadmap, repositorio_user)

    repositorio_comment = InMemoryCommentRepository()
    comment_service = CommentService(repositorio_comment, repositorio_roadmap, repositorio_user)

    yield comment_service, roadmap_service, user_service


def test_comment_create_successfully(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    comment = comment_service.create(user.username, roadmap.id, "comment")

    assert comment.author_username == "marco"
    assert comment.roadmap_id == roadmap.id
    assert comment.text == "comment"


def test_comment_create_missing(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        comment_service.create(None, roadmap.id, "comment")

    with pytest.raises(MissingFieldException):
        comment_service.create(user.username, None, "comment")
    
    with pytest.raises(MissingFieldException):
        comment_service.create(user.username, roadmap.id, None)

def test_comment_create_not_found(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotFoundException):
        comment_service.create("marco2", roadmap.id, "comment")

    with pytest.raises(NotFoundException):
        comment_service.create(user.username, "invalid_roadmap_id", "comment")

def test_comment_find_all_by_roadmap_id_missing(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        comment_service.find_all_by_roadmap_id(None)

def test_comment_delete_by_id_missing(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(MissingFieldException):
        comment_service.delete_by_id(user.username, None)


def test_comment_find_all_by_roadmap_id_not_found(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotFoundException):
        comment_service.find_all_by_roadmap_id("invalid_id")

def test_comment_delete_by_id_not_found(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    with pytest.raises(NotFoundException):
        comment_service.delete_by_id(user.username, "invalid_id")

def test_comment_delete_by_id_unauthorized(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    comment = comment_service.create(user.username, roadmap.id, "comment")

    with pytest.raises(UnauthorizedException):
        comment_service.delete_by_id("another_user", comment.id)

def test_comment_find_all_by_roadmap_id_successfully(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    comment = comment_service.create(user.username, roadmap.id, "comment")

    comments = comment_service.find_all_by_roadmap_id(roadmap.id)

    assert comment.author_username == comments[0].author_username
    assert comment.roadmap_id == comments[0].roadmap_id
    assert comment.text == comments[0].text

def test_comment_delete_by_id_successfully(setup):
    comment_service, roadmap_service, user_service = setup
    user = user_service.create(name="Marco", username="marco", password="123456")

    roadmap = roadmap_service.create(user.username, "titulo", "desc", [[0, 0]], ["tag1"])

    comment = comment_service.create(user.username, roadmap.id, "comment")

    comments = comment_service.find_all_by_roadmap_id(roadmap.id)

    assert len(comments) == 1

    comment_service.delete_by_id(user.username, comment.id)

    comments = comment_service.find_all_by_roadmap_id(roadmap.id)

    assert len(comments) == 0
    