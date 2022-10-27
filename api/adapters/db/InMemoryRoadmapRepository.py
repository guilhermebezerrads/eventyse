import inject 

from domain.interfaces.IRoadmapRepository import IRoadmapRepository
from domain.interfaces.IFollowRepository import IFollowRepository

from domain.models.Roadmap import Roadmap

class InMemoryRoadmapRepository(IRoadmapRepository):
    @inject.autoparams()
    def __init__(self, follows: IFollowRepository) -> None:
        self.follows = follows
        self.roadmaps: list[Roadmap] = []
        self.ratings: list[tuple(str, str, int)] = []
 
    def create(self, roadmap: Roadmap) -> Roadmap:
        self.roadmaps.append(roadmap)
        return roadmap
    

    def is_liked(self, username: str, roadmap_id: str) -> bool:
        for u, r, v in self.ratings:
            if u == username and r == roadmap_id and v == 1:
                return True
        
        return False


    def like(self, username: str, roadmap_id: str) -> None:
        roadmap: Roadmap = self.find_by_id(roadmap_id)

        if self.is_desliked(username, roadmap_id):
            self.ratings.remove((username, roadmap_id, -1))
            roadmap.deslikes -= 1
            self.ratings.append((username, roadmap_id, 1))
            roadmap.likes += 1
        else:
            self.ratings.append((username, roadmap_id, 1))
            roadmap.likes += 1
    

    def is_desliked(self, username: str, roadmap_id: str) -> bool:
        for u, r, v in self.ratings:
            if u == username and r == roadmap_id and v == -1:
                return True
        
        return False


    def deslike(self, username: str, roadmap_id: str) -> None:
        roadmap: Roadmap = self.find_by_id(roadmap_id)

        if self.is_liked(username, roadmap_id):
            self.ratings.remove((username, roadmap_id, 1))
            roadmap.likes -= 1
            self.ratings.append((username, roadmap_id, -1))
            roadmap.deslikes += 1
        else:
            self.ratings.append((username, roadmap_id, -1))
            roadmap.deslikes += 1


    def find_all(self) -> list[Roadmap]:
        return self.roadmaps
    

    def find_by_id(self, roadmap_id: str) -> Roadmap:
        for roadmap in self.roadmaps:
            if roadmap.id == roadmap_id: return roadmap
        return None
    

    def find_all_by_username(self, username: str) -> list[Roadmap]:
        user_roadmaps: list[Roadmap] = []
        for roadmap in self.roadmaps:
            if roadmap.author_username == username: 
                user_roadmaps.append(roadmap)
        return user_roadmaps
    

    def find_all_by_following(self, username: str) -> list[Roadmap]:
        following_roadmaps: list[Roadmap] = []
        following = self.follows.find_all_following(username)
        
        for user in following:
            for roadmap in self.roadmaps:
                if roadmap.author_username == user.username: 
                    following_roadmaps.append(roadmap)

        return following_roadmaps


    def find_all_by_tags(self, tags: list[str]) -> list[Roadmap]:
        tags_roadmaps: list[Roadmap] = []

        for roadmap in self.roadmaps:
            for tag in tags:
                if tag in roadmap.tags:
                    tags_roadmaps.append(roadmap)
                    break
        
        return tags_roadmaps
