from abc import ABC, abstractmethod
from domain.models.Comment import Comment

class ICommentRepository(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, comment_id: str) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, comment_id: str) -> None:
        raise NotImplementedError
