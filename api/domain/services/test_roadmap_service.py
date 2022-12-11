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


