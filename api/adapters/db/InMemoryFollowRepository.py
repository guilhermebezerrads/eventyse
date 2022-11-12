import inject

from domain.ports.IUserRepository import IUserRepository
from domain.ports.IFollowRepository import IFollowRepository

from domain.models.User import User

class InMemoryFollowRepository(IFollowRepository):
    @inject.autoparams()
    def __init__(self, users: IUserRepository) -> None:
        self.followers: list[tuple[str, str]] = []
        self.users: IUserRepository = users
    
    def is_follower(self, username: str, target_username: str) -> bool:
        for u, t in self.followers:
            if (u == username and t == target_username):
                return True
        return False

    def follow(self, username: str, target_username: str) -> bool:        
        self.followers.append((username, target_username))

        user: User = self.users.find_by_username(username)
        target_user: User = self.users.find_by_username(target_username)

        user.following_counter += 1
        target_user.followers_counter += 1

        return True

    def unfollow(self, username: str, target_username: str) -> bool:
        self.followers.remove((username, target_username))

        user: User = self.users.find_by_username(username)
        target_user: User = self.users.find_by_username(target_username)

        user.following_counter -= 1
        target_user.followers_counter -= 1
        return True
        
    
    def find_all_followers(self, username: str) -> list[User]:
        followers = []
        for u, t in self.followers:
            if t == username:
                followers.append(self.users.find_by_username(u))
        return followers

    def find_all_following(self, username: str) -> list[User]:
        following = []
        for u, t in self.followers:
            if u == username:
                following.append(self.users.find_by_username(t))
        return following
