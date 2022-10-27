import inject

from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.AlreadyDeslikedException import AlreadyDeslikedException
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
    
    
    def find_all(self) -> list[Roadmap]:
        return self.roadmap_repository.find_all()


    def find_by_id(self, roadmap_id: str) -> Roadmap:
        if not roadmap_id:
            raise MissingFieldException
        
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)

        if not roadmap:
            raise NotFoundException
        
        return roadmap
    

    def find_all_by_username(self, username: str) -> list[Roadmap]:
        if not username:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)

        if not user:
            raise NotFoundException
        
        return self.roadmap_repository.find_all_by_username(username)
    
    
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        if not username:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username

        if not user:
            raise NotFoundException
        
        return self.roadmap_repository.find_all_by_following(username)


    def find_all_by_tags(self, tag: list[str]) -> list[Roadmap]:
        if not tag:
            raise MissingFieldException
    
        return self.roadmap_repository.find_all_by_tags(tag)


    def create(self, username: str, title: str, description: str, coordinates: list[list[float]], tags: list[str]) -> Roadmap:
        
        if not username or not title or not description or not coordinates or not tags:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)

        if not user:
            raise NotFoundException
        
        roadmap = roadmap_factory(username, title, description, coordinates, tags)

        return self.roadmap_repository.create(roadmap)

    def is_liked(self, username, roadmap_id) -> bool:
        if not username or not roadmap_id:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)

        if not user or not roadmap:
            raise NotFoundException
        
        return self.roadmap_repository.is_liked(username, roadmap_id)


    def like(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)

        if not user or not roadmap:
            raise NotFoundException
        
        if self.roadmap_repository.is_liked(username, roadmap_id):
            raise AlreadyLikedException
        
        self.roadmap_repository.like(username, roadmap_id)

    def is_desliked(self, username, roadmap_id) -> bool:
        if not username or not roadmap_id:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)

        if not user or not roadmap:
            raise NotFoundException
        
        return self.roadmap_repository.is_desliked(username, roadmap_id)


    def deslike(self, username: str, roadmap_id: str) -> None:
        if not username or not roadmap_id:
            raise MissingFieldException
        
        user = self.user_repository.find_by_username(username)
        roadmap = self.roadmap_repository.find_by_id(roadmap_id)
        
        if not user or not roadmap:
            raise NotFoundException
        
        if self.roadmap_repository.is_desliked(username, roadmap_id):
            raise AlreadyDeslikedException
        
        self.roadmap_repository.deslike(username, roadmap_id)

