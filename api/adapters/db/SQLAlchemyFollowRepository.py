import inject
from sqlalchemy.orm import Session

from domain.ports.IUserRepository import IUserRepository
from domain.ports.IFollowRepository import IFollowRepository

from domain.models.User import User

from adapters.db.interfaces.IDatabase import IDatabase
from adapters.db import SQLAlchemy
from adapters.db.utils.mapper import *

class SQLAlchemyFollowRepository(IFollowRepository):
    @inject.autoparams()
    def __init__(self, db: IDatabase) -> None:
        self.db: IDatabase = db
        self.session: Session = db.session

    def is_follower(self, username: str, target_username:str) -> bool:
        follows = self.session.query(SQLAlchemy.following).filter(SQLAlchemy.following.c.username==username, SQLAlchemy.following.c.target_username==target_username).first()

        if follows is None:
            return False

        return True

    def follow(self, username: str, target_username: str) -> bool:
        following = SQLAlchemy.following.insert().values(username=username, target_username=target_username)
        self.session.execute(following)

        user = self.session.query(SQLAlchemy.User).filter_by(username=username).first()
        target_user = self.session.query(SQLAlchemy.User).filter_by(username=target_username).first()

        user.following_counter += 1
        target_user.followers_counter += 1

        self.session.commit()

        return True

    def unfollow(self, username: str, target_username: str) -> bool:
        self.session.query(SQLAlchemy.following).filter(SQLAlchemy.following.c.username==username, SQLAlchemy.following.c.target_username==target_username).delete()

        user = self.session.query(SQLAlchemy.User).filter_by(username=username).first()
        target_user = self.session.query(SQLAlchemy.User).filter_by(username=target_username).first()

        user.following_counter -= 1
        target_user.followers_counter -= 1

        self.session.commit()

        return True

    def find_all_followers(self, username: str) -> list[User]:
        usernames = []
        
        assoc_list = self.session.query(SQLAlchemy.following).filter(SQLAlchemy.following.c.target_username==username).all()

        for assoc in assoc_list:
            usernames.append(assoc.username)
        
        users_db = self.session.query(SQLAlchemy.User).filter(SQLAlchemy.User.username.in_(usernames)).all()

        followers = []
        for user_db in users_db:
            followers.append(user_db_to_user_model(user_db))

        return followers

    def find_all_following(self, username: str) -> list[User]:
        usernames = []

        assoc_list = self.session.query(SQLAlchemy.following).filter(SQLAlchemy.following.c.username==username).all()

        for assoc in assoc_list:
            usernames.append(assoc.target_username)
        
        users_db = self.session.query(SQLAlchemy.User).filter(SQLAlchemy.User.username.in_(usernames)).all()

        following = []
        for user_db in users_db:
            following.append(user_db_to_user_model(user_db))

        return following
