from abc import ABC, abstractmethod
from domain.models.User import User

class IUserService(ABC):
    @abstractmethod
    def already_exists(self, username: int) -> bool:
        pass

    @abstractmethod
    def add(self, user: User) -> bool:
        pass

    @abstractmethod
    def find_all(self) -> list[User]:
        pass
    
    @abstractmethod
    def find_by_username(self, username: int) -> User:
        pass
    
