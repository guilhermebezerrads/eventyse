from abc import ABC, abstractmethod
from domain.entities.User import User

class IUserRepository(ABC):
    @abstractmethod
    def add(user: User):
        pass

    @abstractmethod
    def find_all():
        pass
    
    @abstractmethod
    def find_by_username(username: int):
        pass
    
    @abstractmethod
    def already_exists(username: int):
        pass