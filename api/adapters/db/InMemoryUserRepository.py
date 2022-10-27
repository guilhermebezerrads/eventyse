from domain.interfaces.IUserRepository import IUserRepository

from domain.models.User import User

class InMemoryUserRepository(IUserRepository):
    def __init__(self) -> None:
        self.users: list[User] = []

    def create(self, user: User) -> User:        
        self.users.append(user)

        return user
    
    def find_all(self) -> list[User]:
        return self.users
    
    def find_by_username(self, username: int) -> User:
        for user in self.users:
            if user.username == username: return user
        return None
