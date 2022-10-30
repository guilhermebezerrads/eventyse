from abc import ABC, abstractmethod
from domain.models.User import User

class IUserService(ABC):
    @abstractmethod
    def already_exists(self, username) -> bool:
        pass
    
    @abstractmethod
    def create(self, name: str, username: str, password: str) -> User:
        pass

    @abstractmethod
    def is_password_correct(self, user: User, try_password: str):
        pass
    
    @abstractmethod
    def login(self, username: str, try_password: str) -> User:
        pass

    @abstractmethod
    def find_all(self) -> list[User]:
        pass
    
    @abstractmethod
    def find_by_username(self, username: int) -> User:
        pass
    