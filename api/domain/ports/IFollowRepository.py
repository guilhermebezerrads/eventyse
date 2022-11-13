from abc import ABC, abstractmethod
from domain.models.User import User

class IFollowRepository(ABC):
    @abstractmethod
    def is_follower(self, username: str, target_username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def follow(self, username: str, target_username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unfollow(self, username: str, target_username: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def find_all_followers(self, username: str) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def find_all_following(self, username: str) -> list[User]:
        raise NotImplementedError
    