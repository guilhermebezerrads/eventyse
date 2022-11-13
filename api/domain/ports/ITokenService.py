from abc import ABC, abstractmethod

from domain.models.User import User

class ITokenService(ABC):
    @abstractmethod
    def authenticate_token(self, token: str):
        raise NotImplementedError
    
    @abstractmethod
    def create_token(self, user: User):
        raise NotImplementedError
