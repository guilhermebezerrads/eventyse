import SQLAlchemy
from SQLAlchemyRoadmapRepository import SQLAlchemyRoadmapRepository
from SQLAlchemyUserRepository import SQLAlchemyUserRepository
from SQLAlchemyFollowRepository import SQLAlchemyFollowRepository

from domain.models.Roadmap import roadmap_factory
from domain.models.User import user_factory

import pytest

@pytest.fixture
def createDB():
    db = SQLAlchemy.SQLiteDatabase('sqlite:///test.sqlite?check_same_thread=False')
    repoRoadmap = SQLAlchemyRoadmapRepository(db)
    repoUser = SQLAlchemyUserRepository(db)
    repoFollow = SQLAlchemyFollowRepository(db)

    user1 = user_factory(
        name='carlos',
        username='carlinhos',
        password_hash='1234'.encode(),
        password_salt='12345'.encode(),
    )

    user2 = user_factory(
        name='melanie',
        username='melanina',
        password_hash='1234'.encode(),
        password_salt='12345'.encode(),
    )

    roadmap1 = roadmap_factory(
        author_username = 'carlinhos',
        title = 'mapa1',
        coordinates=[[32.4234, -123.432], [442.3, -23.67]],
        description = 'primeiro mapa',
        tags = ['bh', 'lagoa'],
    )

    roadmap2 = roadmap_factory(
        author_username = 'carlinhos',
        title = 'mapa2',
        coordinates=[[3212.4234, -1233.432], [4492.3, -253.67]],
        description = 'segundo mapa',
        tags = ['bh', 'centro'],
    )

    roadmap3 = roadmap_factory(
        author_username = 'melanina',
        title = 'mapa3',
        coordinates=[[9.4234, -19233.432], [4992.3, -553.67]],
        description = 'mapa da melanie',
        tags = ['itauba', 'centro'],
    )

    repoUser.create(user1)
    repoUser.create(user2)

    repoRoadmap.create(roadmap1)
    repoRoadmap.create(roadmap2)
    repoRoadmap.create(roadmap3)

    repoFollow.follow('carlinhos', 'melanina')
    repoFollow.follow('melanina', 'carlinhos')

    yield repoRoadmap

    repoRoadmap.session.query(SQLAlchemy.Roadmap).delete()
    repoRoadmap.session.commit()

    repoFollow.session.query(SQLAlchemy.following).delete()
    repoFollow.session.commit()

    repoUser.session.query(SQLAlchemy.User).delete()
    repoUser.session.commit()

    repoUser.session.query(SQLAlchemy.Tag).delete()
    repoUser.session.commit()

@pytest.mark.integtest
def test_find_by_id(createDB):
    roadmap = roadmap_factory(
        author_username = 'carlinhos',
        title = 'mapaN',
        coordinates=[[32.4234, -123.432], [442.3, -23.67]],
        description = 'N mapa',
        tags = ['bh', 'lagoa'],
    )

    createDB.create(roadmap)

    roadmap_model = createDB.find_by_id(roadmap.id)
    assert roadmap_model.id == roadmap.id

    roadmap_model = createDB.find_by_id(-1)
    assert roadmap_model == None

@pytest.mark.integtest
def test_find_by_username(createDB):
    roadmaps = createDB.find_all_by_username('carlinhos')
    assert len(roadmaps) == 2

    roadmaps = createDB.find_all()
    assert len(roadmaps) == 3

@pytest.mark.integtest
def test_find_by_following(createDB):
    roadmaps_m = createDB.find_all_by_following('melanina')
    roadmaps_c = createDB.find_all_by_following('carlinhos')

    assert len(roadmaps_m) == 2
    assert len(roadmaps_c) == 1

@pytest.mark.integtest
def test_find_by_tags(createDB):
    roadmaps = createDB.find_all_by_tags(['bh'])
    assert len(roadmaps) == 2

@pytest.mark.integtest
def test_like(createDB):
    roadmap = createDB.find_all_by_username('melanina')[0]

    createDB.add_like('carlinhos', roadmap.id)
    assert createDB.is_liked('carlinhos', roadmap.id) == True

    createDB.remove_like('carlinhos', roadmap.id)
    assert createDB.is_liked('carlinhos', roadmap.id) == False

@pytest.mark.integtest
def test_dislike(createDB):
    roadmap = createDB.find_all_by_username('melanina')[0]
    
    createDB.add_dislike('carlinhos', roadmap.id)
    assert createDB.is_disliked('carlinhos', roadmap.id) == True

    createDB.remove_dislike('carlinhos', roadmap.id)
    assert createDB.is_disliked('carlinhos', roadmap.id) == False

@pytest.mark.integtest
def test_like_and_dislike(createDB):
    roadmap = createDB.find_all_by_username('melanina')[0]

    createDB.add_like('carlinhos', roadmap.id)
    createDB.add_dislike('carlinhos', roadmap.id)

    assert createDB.is_disliked('carlinhos', roadmap.id) == True

    createDB.add_dislike('carlinhos', roadmap.id)
    createDB.add_like('carlinhos', roadmap.id)

    assert createDB.is_liked('carlinhos', roadmap.id) == True
