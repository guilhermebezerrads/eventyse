from domain.interfaces.IUserRepository import IUserRepository
from domain.models.User import User

class InMemoryUserRepository(IUserRepository):
    def __init__(self) -> None:
        self.users: list[User] = []

    def already_exists(self, username) -> bool:
        for user in self.users:
            if user.username == username: return True
        return False

    def add(self, user: User) -> bool:
        if self.already_exists(user.username): 
            return False
        
        self.users.append(user)
        return True
    
    def find_all(self) -> list[User]:
        return self.users
    
    def find_by_username(self, username: int) -> User:
        for user in self.users:
            if user.username == username: return user
        return None
