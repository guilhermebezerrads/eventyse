import inject

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.SameUserException import SameUserException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.AlreadyFollowException import AlreadyFollowException
from domain.exceptions.NotFollowerException import NotFollowerException

from domain.interfaces.IFollowRepository import IFollowRepository
from domain.interfaces.IUserRepository import IUserRepository

from domain.models.User import User

class FollowService():
    @inject.autoparams()
    def __init__(self, follow_repository: IFollowRepository, user_repository: IUserRepository):
        self.follow_repository: IFollowRepository = follow_repository
        self.user_repository: IUserRepository = user_repository
    
    def is_follower(self, username: str, target_username: str) -> bool:
        if not username or not target_username:
            raise MissingFieldException
        
        if username == target_username:
            raise SameUserException

        current_user: User = self.user_repository.find_by_username(username)
        target_user: User = self.user_repository.find_by_username(target_username)

        if not current_user or not target_user:
            raise NotFoundException
        
        return self.follow_repository.is_follower(username, target_username)

    def follow(self, username: str, target_username: str) -> bool:
        if not username or not target_username:
            raise MissingFieldException
        
        if username == target_username:
            raise SameUserException
        
        current_user: User = self.user_repository.find_by_username(username)
        target_user: User = self.user_repository.find_by_username(target_username)

        if not current_user or not target_user:
            raise NotFoundException
        
        if self.is_follower(username, target_username):
            raise AlreadyFollowException
        
        return self.follow_repository.follow(username, target_username)

    def unfollow(self, username: str, target_username: str) -> bool:
        if not username or not target_username:
            raise MissingFieldException
        
        if username == target_username:
            raise SameUserException

        current_user: User = self.user_repository.find_by_username(username)
        target_user: User = self.user_repository.find_by_username(target_username)
        
        if not current_user or not target_user:
            raise NotFoundException
        
        if not self.is_follower(username, target_username):
            raise NotFollowerException

        return self.follow_repository.unfollow(username, target_username)
    
    def find_all_followers(self, username: str) -> list[User]:
        if not username:
            raise MissingFieldException
        
        user: User = self.user_repository.find_by_username(username)

        if not user:
            raise NotFoundException
        
        return self.follow_repository.find_all_followers(username)
  
    def find_all_following(self, username: str) -> list[User]:
        if not username:
            raise MissingFieldException
        
        user: User = self.user_repository.find_by_username(username)

        if not user:
            raise NotFoundException
        
        return self.follow_repository.find_all_following(username)
