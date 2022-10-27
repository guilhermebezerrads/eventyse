import inject

from domain.interfaces.IFollowRepository import IFollowRepository

from domain.models.User import User

class FollowService():
    @inject.autoparams()
    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository: IFollowRepository = follow_repository
    
    def already_follow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.already_follow(username, target_username)

    def follow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.follow(username, target_username)

    def unfollow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.unfollow(username, target_username)
    
    def find_all_followers(self, username: str) -> list[User]:
        return self.follow_repository.find_all_followers(username)
  
    def find_all_following(self, username: str) -> list[User]:
        return self.follow_repository.find_all_following(username)
        