from abc import ABC, abstractmethod
from domain.models.User import User

class IFollowerRepository(ABC):
    @abstractmethod
    def already_follow(self, username: str, target_username: str) -> bool:
        pass

    @abstractmethod
    def add_follow(self, username: str, target_username: str) -> bool:
        pass

    @abstractmethod
    def remove_follow(self, username: str, target_username: str) -> bool:
        pass
    
    @abstractmethod
    def find_all_followers(self, username: str) -> list[User]:
        pass

    @abstractmethod
    def find_all_following(self, username: str) -> list[User]:
        pass
    