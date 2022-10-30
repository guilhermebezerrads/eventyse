from abc import ABC, abstractmethod
from domain.models.Roadmap import Roadmap

class IRoadmapService(ABC):
    @abstractmethod
    def create(self, username: str, title: str, description: str, coordinates: list[list[float]], tags: list[str]) -> Roadmap:
        pass
    
    @abstractmethod
    def find_all(self) -> list[Roadmap]:
        pass

    @abstractmethod
    def find_by_id(self, roadmap_id: str) -> Roadmap:
        pass
    
    @abstractmethod
    def find_all_by_username(self, username: str) -> list[Roadmap]:
        pass
    
    @abstractmethod    
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        pass

    @abstractmethod
    def find_all_by_tags(self, tags: list[str]) -> list[Roadmap]:
        pass

    @abstractmethod
    def is_liked(self, username, roadmap_id) -> bool:
        pass

    @abstractmethod
    def add_like(self, username: str, roadmap_id: str) -> None:
        pass
    
    @abstractmethod 
    def remove_like(self, username: str, roadmap_id: str) -> None:
        pass

    @abstractmethod
    def is_disliked(self, username, roadmap_id) -> bool:
        pass

    @abstractmethod
    def add_dislike(self, username: str, roadmap_id: str) -> None:
        pass
    
    @abstractmethod
    def remove_dislike(self, username: str, roadmap_id: str) -> None:
        pass
