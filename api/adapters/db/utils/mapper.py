from domain.models.User import User
from domain.models.Comment import Comment

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

def comment_db_to_comment_model(comment_db: SQLAlchemy.Comment) -> Comment:
    return Comment(
        id = comment_db.id,
        author_username = comment_db.author_username,
        roadmap_id = comment_db.roadmap_id,
        text = comment_db.text,
        created_date = comment_db.created_date
    )

def comment_model_to_comment_db(comment: Comment) -> SQLAlchemy.Comment:
    return SQLAlchemy.Comment(
        id = comment.id,
        author_username = comment.author_username,
        roadmap_id = comment.roadmap_id,
        text = comment.text,
        created_date = comment.created_date
    )
