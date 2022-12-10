import SQLAlchemy
from SQLAlchemyRoadmapRepository import SQLAlchemyRoadmapRepository
from SQLAlchemyUserRepository import SQLAlchemyUserRepository
from SQLAlchemyCommentRepository import SQLAlchemyCommentRepository

from domain.models.Roadmap import roadmap_factory
from domain.models.User import user_factory
from domain.models.Comment import comment_factory

import pytest

@pytest.fixture
def createDB():
    db = SQLAlchemy.SQLiteDatabase('sqlite:///test.sqlite?check_same_thread=False')
    repoRoadmap = SQLAlchemyRoadmapRepository(db)
    repoUser = SQLAlchemyUserRepository(db)
    repoComment = SQLAlchemyCommentRepository(db)

    user1 = user_factory(
        name='carlos',
        username='carlinhos',
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

    comment1 = comment_factory(
        author_username = 'carlinhos', 
        roadmap_id = roadmap1.id, 
        text = 'um belo post', 
    )

    comment2 = comment_factory(
        author_username = 'carlinhos', 
        roadmap_id = roadmap1.id, 
        text = 'um post', 
    )

    repoUser.create(user1)
    repoRoadmap.create(roadmap1)
    repoComment.create(comment1)
    repoComment.create(comment2)

    yield [repoComment, repoRoadmap, comment1]

    repoRoadmap.session.query(SQLAlchemy.Roadmap).delete()
    repoRoadmap.session.commit()

    repoUser.session.query(SQLAlchemy.User).delete()
    repoUser.session.commit()

    repoUser.session.query(SQLAlchemy.Comment).delete()
    repoUser.session.commit()

@pytest.mark.integtest
def test_find_by_id(createDB):
    comment_model = createDB[0].find_by_id(createDB[2].id)
    assert comment_model.id == createDB[2].id

    comment_model = createDB[0].find_by_id(-1)
    assert comment_model == None

@pytest.mark.integtest
def test_find_all_by_roadmap_id(createDB):
    roadmap = createDB[1].find_all_by_username('carlinhos')[0]

    comments = createDB[0].find_all_by_roadmap_id(roadmap.id)

    assert len(comments) == 2

@pytest.mark.integtest
def test_delete_by_id(createDB):
    roadmap = createDB[1].find_all_by_username('carlinhos')[0]

    createDB[0].delete_by_id(createDB[2].id)

    comments = createDB[0].find_all_by_roadmap_id(roadmap.id)
    assert len(comments) == 1
