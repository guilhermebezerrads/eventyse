import inject
import bcrypt

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.UsernameAlreadyExistsException import UsernameAlreadyExistsException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException

from domain.interfaces.IUserRepository import IUserRepository

from domain.models.User import User, user_factory


class UserService():
    @inject.autoparams()
    def __init__(self, user_repository: IUserRepository):
        self.user_repository: IUserRepository = user_repository


    def already_exists(self, username) -> bool:
        return self.user_repository.find_by_username(username) != None
    

    def create(self, name: str, username: str, password: str) -> User:
        if not name or not username or not password:
            raise MissingFieldException
        
        if self.already_exists(username):
            raise UsernameAlreadyExistsException()
        
        password: bytes = password.encode()
        password_salt: bytes = bcrypt.gensalt()
        password_hash: bytes = bcrypt.hashpw(password, password_salt)

        user = user_factory(name, username, password_hash, password_salt)
        return self.user_repository.create(user)


    def is_password_correct(self, user: User, try_password: str):
        try_password_hash = bcrypt.hashpw(try_password.encode(), user.password_salt.encode())
        return try_password_hash.decode() == user.password_hash
    

    def login(self, username: str, try_password: str) -> User:
        if not username or not try_password:
            raise MissingFieldException

        user = self.find_by_username(username)
        if not user:
            raise NotFoundException
        
        if not self.is_password_correct(user, try_password):
            raise UnauthorizedException
        
        return user


    def find_all(self) -> list[User]:
        return self.user_repository.find_all()
    

    def find_by_username(self, username: int) -> User:
        if not username:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)
        if not user:
            raise NotFoundException
        
        return user
    