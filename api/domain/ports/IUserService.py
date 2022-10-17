from abc import ABC, abstractmethod
from domain.entities.User import User

class IUserService(ABC):
    @abstractmethod
    def already_exists(username: int):
        pass

    @abstractmethod
    def add(user: User):
        pass

    @abstractmethod
    def find_all():
        pass
    
    @abstractmethod
    def find_by_username(username: int):
        pass
    
