import inject

from domain.interfaces.IUserRepository import IUserRepository

from domain.models.User import User

class UserService():
    @inject.autoparams()
    def __init__(self, user_repository: IUserRepository):
        self.user_repository: IUserRepository = user_repository

    def exists(self, username) -> bool:
        return self.user_repository.exists(username)
    
    def add(self, user: User) -> bool:
        return self.user_repository.add(user)

    def find_all(self) -> list[User]:
        return self.user_repository.find_all()
    
    def find_by_username(self, username: int) -> User:
        return self.user_repository.find_by_username(username)
    