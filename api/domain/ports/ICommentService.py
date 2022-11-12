from abc import ABC, abstractmethod
from domain.models.Comment import Comment

class ICommentService(ABC):
    @abstractmethod
    def create(self, username: str, roadmap_id: str, text: str) -> Comment:
        pass

    @abstractmethod
    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        pass

    @abstractmethod
    def delete_by_id(self, username: str, comment_id: str) -> None:
        pass
