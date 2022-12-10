import SQLAlchemy
from SQLAlchemyUserRepository import SQLAlchemyUserRepository
from domain.models.User import user_factory

import pytest

@pytest.fixture
def createDB():
    db = SQLAlchemy.SQLiteDatabase('sqlite:///test.sqlite?check_same_thread=False')
    repo = SQLAlchemyUserRepository(db)

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

    repo.create(user1)
    repo.create(user2)
    repo.create(user3)

    yield repo

    repo.session.query(SQLAlchemy.User).delete()
    repo.session.commit()

@pytest.mark.integtest
def test_find_existing_username(createDB):
    user_model = createDB.find_by_username('carlinhos')
    assert user_model.username == 'carlinhos'

@pytest.mark.integtest
def test_find_non_existing_username(createDB):
    user_model = createDB.find_by_username('carlitos')
    assert user_model == None

@pytest.mark.integtest
def test_find_all(createDB):
    assert len(createDB.find_all()) == 3