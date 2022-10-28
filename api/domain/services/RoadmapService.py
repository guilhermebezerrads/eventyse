import inject

from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.AlreadyDislikedException import AlreadyDislikedException
from domain.exceptions.NotLikedException import NotLikedException
from domain.exceptions.NotDislikedException import NotDislikedException
from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.interfaces.IRoadmapRepository import IRoadmapRepository
from domain.interfaces.IUserRepository import IUserRepository

from domain.models.Roadmap import Roadmap, roadmap_factory

class RoadmapService():
    @inject.autoparams()
    def __init__(self, roadmap_repository: IRoadmapRepository, user_repository: IUserRepository):
        self.roadmap_repository: IRoadmapRepository = roadmap_repository
        self.user_repository: IUserRepository = user_repository
    
    
    def create(self, username: str, title: str, description: str, coordinates: list[list[float]], tags: list[str]) -> Roadmap:
        if not username or not title or not description or not coordinates or not tags:
            raise MissingFieldException('missing username, title, description, coordinates or tags field')
        
        user = self.user_repository.find_by_username(username)
        if not user:
            raise NotFoundException('user not found')
        
        roadmap = roadmap_factory(username, title, description, coordinates, tags)
        return self.roadmap_repository.create(roadmap)
    

    def find_all(self) -> list[Roadmap]:
        return self.roadmap_repository.find_all()


    def find_by_id(self, roadmap_id: str) -> Roadmap:
        if not roadmap_id:
            raise MissingFieldException('missing roadmap_id')

        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not roadmap:
            raise NotFoundException('roadmap not found')
        
        return roadmap
    

    def find_all_by_username(self, username: str) -> list[Roadmap]:
        if not username:
            raise MissingFieldException('missing username field')
        
        user = self.user_repository.find_by_username(username)
        if not user:
            raise NotFoundException('user not found')
        
        return self.roadmap_repository.find_all_by_username(username)
    
    
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        if not username:
            raise MissingFieldException('missing username field')
        
        user = self.user_repository.find_by_username(username)
        if not user:
            raise NotFoundException('user not found')
        
        return self.roadmap_repository.find_all_by_following(username)


    def find_all_by_tags(self, tags: list[str]) -> list[Roadmap]:
        if not tags:
            raise MissingFieldException('missing tags field')
    
        return self.roadmap_repository.find_all_by_tags(tags)


    def is_liked(self, username, roadmap_id) -> bool:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id field')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        return self.roadmap_repository.is_liked(username, roadmap_id)


    def add_like(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        if self.roadmap_repository.is_liked(username, roadmap_id):
            raise AlreadyLikedException('roadmap already liked')
        
        self.roadmap_repository.add_like(username, roadmap_id)
    
    
    def remove_like(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        if not self.roadmap_repository.is_liked(username, roadmap_id):
            raise NotLikedException('roadmap must to be liked')
        
        self.roadmap_repository.remove_like(username, roadmap_id)


    def is_disliked(self, username, roadmap_id) -> bool:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id field')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        return self.roadmap_repository.is_disliked(username, roadmap_id)


    def add_dislike(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id field')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        if self.roadmap_repository.is_disliked(username, roadmap_id):
            raise AlreadyDislikedException('roadmap already disliked')
        
        self.roadmap_repository.add_dislike(username, roadmap_id)
    
    
    def remove_dislike(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException('missing username or roadmap_id field')
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        if not user or not roadmap:
            raise NotFoundException('user or roadmap not found')
        
        if not self.roadmap_repository.is_disliked(username, roadmap_id):
            raise NotDislikedException('roadmap must to be disliked')
        
        self.roadmap_repository.remove_dislike(username, roadmap_id)
