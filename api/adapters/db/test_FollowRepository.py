import SQLAlchemy
from SQLAlchemyFollowRepository import SQLAlchemyFollowRepository
from SQLAlchemyUserRepository import SQLAlchemyUserRepository

from domain.models.User import user_factory

import pytest

@pytest.fixture
def createDB():
    db = SQLAlchemy.SQLiteDatabase('sqlite:///test.sqlite?check_same_thread=False')
    repoFollow = SQLAlchemyFollowRepository(db)
    repoUser = SQLAlchemyUserRepository(db)

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

    user3 = user_factory(
        name='vara',
        username='varinha',
        password_hash='1234'.encode(),
        password_salt='12345'.encode(),
    )

    repoUser.create(user1)
    repoUser.create(user2)
    repoUser.create(user3)

    yield repoFollow

    repoFollow.session.query(SQLAlchemy.following).delete()
    repoFollow.session.commit()

    repoUser.session.query(SQLAlchemy.User).delete()
    repoUser.session.commit()

@pytest.mark.integtest
def test_follow(createDB):
    createDB.follow('carlinhos', 'melanina')

    followers = createDB.find_all_followers('melanina')
    following = createDB.find_all_following('carlinhos')

    assert followers[0].username == 'carlinhos' 
    assert following[0].username == 'melanina'

@pytest.mark.integtest
def test_unfollow(createDB):
    createDB.follow('carlinhos', 'melanina')
    createDB.follow('carlinhos', 'varinha')
    createDB.unfollow('carlinhos', 'melanina')

    following = createDB.find_all_following('carlinhos')
    assert createDB.is_follower('carlinhos', 'varinha') == True
    assert createDB.is_follower('carlinhos', 'melanina') == False
