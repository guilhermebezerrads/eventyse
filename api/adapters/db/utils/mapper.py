from domain.models.User import User
from adapters.db import SQLAlchemy

def user_db_to_user_model(user_db: SQLAlchemy.User) -> User:

    return User(
        id=user_db.id,
        name=user_db.name,
        username=user_db.username,
        password_hash=user_db.password_hash,
        password_salt=user_db.password_salt,
        followers_counter=user_db.followers_counter,
        following_counter=user_db.following_counter
    )

def user_model_to_user_db(user: User) -> SQLAlchemy.User:

    return SQLAlchemy.User(
        id=user.id,
        name=user.name,
        username=user.username,
        password_hash=user.password_hash,
        password_salt=user.password_salt,
        followers_counter=user.followers_counter,
        following_counter=user.following_counter
    )
