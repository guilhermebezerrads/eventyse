from abc import ABC, abstractmethod
from domain.models.Roadmap import Roadmap

class IRoadmapRepository(ABC):
    @abstractmethod
    def create(self, roadmap: Roadmap) -> Roadmap:
        pass

    @abstractmethod
    def find_all(self) -> list[Roadmap]:
        pass
    
    @abstractmethod
    def find_by_id(self, roadmap_id: str) -> Roadmap:
        pass
    
    @abstractmethod
    def is_liked(self, username: str, roadmap_id: str) -> bool:
        pass

    @abstractmethod
    def like(self, username: str, roadmap_id: str) -> None:
        pass

    @abstractmethod
    def is_desliked(self, username: str, roadmap_id: str) -> bool:
        pass

    @abstractmethod
    def deslike(self, username: str, roadmap_id: str) -> None:
        pass
    
    @abstractmethod
    def find_all_by_username(self, username: str) -> list[Roadmap]:
        pass
    
    @abstractmethod
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        pass

    @abstractmethod
    def find_all_by_tags(self, tag: list[str]) -> list[Roadmap]:
        pass
