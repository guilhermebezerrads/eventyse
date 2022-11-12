from abc import ABC, abstractmethod
from domain.models.Comment import Comment

class ICommentRepository(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def find_by_id(self, comment_id: str) -> Comment:
        pass

    @abstractmethod
    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        pass

    @abstractmethod
    def delete_by_id(self, comment_id: str) -> None:
        pass
