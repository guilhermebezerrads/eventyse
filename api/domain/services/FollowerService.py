import inject

from domain.interfaces.IFollowerRepository import IFollowerRepository

from domain.models.User import User

class FollowerService():
    @inject.autoparams()
    def __init__(self, follow_repository: IFollowerRepository):
        self.follow_repository: IFollowerRepository = follow_repository
    
    def already_follow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.already_follow(username, target_username)

    def add_follow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.add_follow(username, target_username)

    def remove_follow(self, username: str, target_username: str) -> bool:
        return self.follow_repository.remove_follow(username, target_username)
    
    def find_all_followers(self, username: str) -> list[User]:
        return self.follow_repository.find_all_followers(username)
  
    def find_all_following(self, username: str) -> list[User]:
        return self.follow_repository.find_all_following(username)
        