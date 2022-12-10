import pytest
import os
from dotenv import load_dotenv

from SQLAlchemy import SQLiteDatabase, User
from SQLAlchemyUserRepository import SQLAlchemyUserRepository
from domain.models.User import User

@pytest.fixture
def createDB():
    load_dotenv()
    db = SQLiteDatabase(os.getenv('SQLALCHEMY_DATABASE_URI'))    
    repo = SQLAlchemyUserRepository(db)

    return repo

def testCreateUser(createDB):
    user = User(
        id=1,
        name='carlos',
        username='carlinhos',
        password_hash='1234',
        password_salt='12345',
        followers_counter=0,
        following_counter=0
    )

    createDB.repo.create(user)

    assert createDB.repo.session.query(User).filter_by(username='carlinhos').first()