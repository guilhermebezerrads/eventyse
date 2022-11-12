import inject
from sqlalchemy.orm import Session

from domain.ports.IUserRepository import IUserRepository
from domain.models.User import User

from adapters.db.interfaces.IDatabase import IDatabase
from adapters.db import SQLAlchemy
from adapters.db.utils.mapper import *

class SQLAlchemyUserRepository(IUserRepository):
    @inject.autoparams()
    def __init__(self, db: IDatabase) -> None:
        self.db: IDatabase = db
        self.session: Session = db.session

    def create(self, user: User) -> User:
        user_db = user_model_to_user_db(user)

        self.session.add(user_db)
        self.session.commit()

        return user
    
    def find_all(self) -> list[User]:
        users = []
        users_db = self.session.query(SQLAlchemy.User).all()

        for user_db in users_db:
            users.append(user_db_to_user_model(user_db))

        return users
    
    def find_by_username(self, username: str) -> User:
        user_db = self.session.query(SQLAlchemy.User).filter_by(username=username).first()
        
        if user_db:
            return user_db_to_user_model(user_db)

        return None
