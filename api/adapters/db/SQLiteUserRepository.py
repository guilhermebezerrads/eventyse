import inject
from sqlalchemy import select

from domain.ports.IUserRepository import IUserRepository

from adapters.db import SQLiteDB
from domain.models.User import User
from domain.ports.IDatabase import IDatabase

class SQLiteUserRepository(IUserRepository):
    @inject.autoparams()
    def __init__(self, db: IDatabase) -> None:
        self.db = db

    def create(self, user: User) -> User:
        user_db = SQLiteDB.User()
        user_db.id = user.id
        user_db.name = user.name
        user_db.username = user.username
        user_db.password_hash = user.password_hash
        user_db.password_salt = user.password_salt
        user_db.followers_counter = user.followers_counter
        user_db.following_counter = user.following_counter

        self.db.session.add(user_db)
        self.db.session.commit()

        return user
    
    def find_all(self) -> list[User]:
        return self.users
    
    def find_by_username(self, username: str) -> User:
        user_db = self.db.session.query(SQLiteDB.User).filter_by(username=username).all()
        print("find_by_username")
        #print(user_db)
        if user_db:
            user_db = user_db[0]
            user = User(
                id = user_db.id,
                name = user_db.name,
                username = user_db.username,
                password_hash = user_db.password_hash,
                password_salt = user_db.password_salt,
                followers_counter = user_db.followers_counter,
                following_counter = user_db.following_counter
            )
            return user

        return None
