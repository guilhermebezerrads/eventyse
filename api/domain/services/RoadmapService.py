import inject

from domain.interfaces.IRoadmapRepository import IRoadmapRepository

from domain.models.Roadmap import Roadmap

class RoadmapService():
    @inject.autoparams()
    def __init__(self, roadmap_repository: IRoadmapRepository):
        self.roadmap_repository: IRoadmapRepository = roadmap_repository
    
    def add(self, roadmap: Roadmap) -> bool:
        return self.roadmap_repository.add(roadmap)

    def like(self, username: str, roadmap_id: str) -> bool:
        return self.roadmap_repository.like(username, roadmap_id)

    def deslike(self, username: str, roadmap_id: str) -> bool:
        return self.roadmap_repository.deslike(username, roadmap_id)

    def find_all(self) -> list[Roadmap]:
        return self.roadmap_repository.find_all()
    
    def find_by_id(self, roadmap_id: str) -> Roadmap:
        return self.roadmap_repository.find_by_id(roadmap_id)
    
    def find_all_by_username(self, username: str) -> list[Roadmap]:
        return self.roadmap_repository.find_all_by_username(username)
    
    def find_all_by_following(self, username: str) -> list[Roadmap]:
        return self.roadmap_repository.find_all_by_following(username)

    def find_all_by_tags(self, tag: list[str]) -> list[Roadmap]:
        return self.roadmap_repository.find_all_by_tags(tag)
