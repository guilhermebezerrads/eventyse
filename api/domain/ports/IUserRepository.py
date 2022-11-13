from abc import ABC, abstractmethod
from domain.models.User import User

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[User]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError
    