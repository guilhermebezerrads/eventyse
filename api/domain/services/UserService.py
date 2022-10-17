from injector import inject

from domain.ports.IUserService import IUserService
from domain.ports.IUserRepository import IUserRepository

from domain.entities.User import User

class UserService(IUserService):
    @inject
    def __init__(self, users: IUserRepository):
        self.user_repository: IUserRepository = users

    def already_exists(self, username) -> bool:
        return self.user_repository.already_exists(username)
    
    def add(self, user: User) -> bool:
        return self.user_repository.add(user)

    def find_all(self) -> list[User]:
        return self.user_repository.find_all()
    
    def find_by_username(self, username: int) -> User:
        return self.user_repository.find_by_username(username)
    