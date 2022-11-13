from abc import ABC, abstractmethod
from domain.models.Roadmap import Roadmap

class IRoadmapRepository(ABC):
    @abstractmethod
    def create(self, roadmap: Roadmap) -> Roadmap:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Roadmap]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, roadmap_id: str) -> Roadmap:
        raise NotImplementedError
    
    @abstractmethod
    def is_liked(self, username: str, roadmap_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_like(self, username: str, roadmap_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_like(self, username: str, roadmap_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_disliked(self, username: str, roadmap_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_dislike(self, username: str, roadmap_id: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def remove_dislike(self, username: str, roadmap_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_username(self, username: str) -> list[Roadmap]:
        raise NotImplementedError
    
    @abstractmethod
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_tags(self, tags: list[str]) -> list[Roadmap]:
        raise NotImplementedError
