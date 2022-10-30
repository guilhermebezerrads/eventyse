import inject

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.ports.ICommentService import ICommentService
from domain.ports.ICommentRepository import ICommentRepository
from domain.ports.IRoadmapRepository import IRoadmapRepository
from domain.ports.IUserRepository import IUserRepository

from domain.models.Comment import Comment, comment_factory

class CommentService(ICommentService):
    @inject.autoparams()
    def __init__(self, comment_repository: ICommentRepository, roadmap_repository: IRoadmapRepository, user_repository: IUserRepository):
        self.comment_repository: ICommentRepository = comment_repository
        self.roadmap_repository: IRoadmapRepository = roadmap_repository
        self.user_repository: IUserRepository = user_repository
    

    def create(self, username: str, roadmap_id: str, text: str) -> Comment:
        if not username or not roadmap_id or not text:
            raise MissingFieldException('missing username, roadmap_id or text field')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('roadmap not found')
        
        comment = comment_factory(username, roadmap_id, text)
        return self.comment_repository.create(comment)


    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        if not roadmap_id:
            return MissingFieldException('missing roadmap_id field')
        
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not roadmap:
            raise NotFoundException('roadmap not found')

        return self.comment_repository.find_all_by_roadmap_id(roadmap_id)
