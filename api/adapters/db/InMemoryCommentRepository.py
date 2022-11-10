from domain.ports.ICommentRepository import ICommentRepository

from domain.models.Comment import Comment

class InMemoryCommentRepository(ICommentRepository):
    def __init__(self) -> None:
        self.comments: list[Comment] = []


    def create(self, comment: Comment) -> Comment:
        self.comments.append(comment)
        return comment
    
    
    def find_by_id(self, comment_id: str) -> Comment:
        for comment in self.comments:
            if comment.id == comment_id:
                return comment
        return None


    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        roadmap_comments: list[Comment] = []
        for comment in self.comments:
            if comment.roadmap_id == roadmap_id:
                roadmap_comments.append(comment)
        return roadmap_comments

    def delete_by_id(self, comment_id: str) -> None:
        comment_to_delete: Comment = None
        for comment in self.comments:
            if comment.id == comment_id:
                comment_to_delete = comment
                break

        self.comments.remove(comment_to_delete)

        return None
