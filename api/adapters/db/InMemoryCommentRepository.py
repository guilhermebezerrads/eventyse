from domain.ports.ICommentRepository import ICommentRepository

from domain.models.Comment import Comment

class InMemoryCommentRepository(ICommentRepository):
    def __init__(self) -> None:
        self.comments: list[Comment] = []


    def create(self, comment: Comment) -> Comment:
        self.comments.append(comment)
        return comment


    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        roadmap_comments: list[Comment] = []
        for comment in self.comments:
            if comment.roadmap_id == roadmap_id:
                roadmap_comments.append(comment)
        return roadmap_comments
