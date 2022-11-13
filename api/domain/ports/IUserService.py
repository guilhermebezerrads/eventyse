from abc import ABC, abstractmethod
from domain.models.User import User

class IUserService(ABC):
    @abstractmethod
    def already_exists(self, username) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def create(self, name: str, username: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def is_password_correct(self, user: User, try_password: str):
        raise NotImplementedError
    
    @abstractmethod
    def login(self, username: str, try_password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[User]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_username(self, username: int) -> User:
        raise NotImplementedError
    