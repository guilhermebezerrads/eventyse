from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.exceptions.AlreadyFollowException import AlreadyFollowException
from domain.exceptions.NotFollowerException import NotFollowerException
from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.SameUserException import SameUserException

from domain.models.User import User
from domain.models.Error import Error

from domain.services.FollowService import FollowService
from domain.services.UserService import UserService

from ..auth import token_required

@inject.autoparams()
def create_follows_blueprint(user_service: UserService, follow_service: FollowService) -> Blueprint:
    follows_blueprint = Blueprint('follows', __name__)

    @follows_blueprint.route('/users/follow/<target_username>', methods=['GET'])
    @token_required
    def is_follower(current_user: User, target_username: str):
        username: str = current_user.username

        try:
            is_follower = follow_service.is_follower(username, target_username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except SameUserException:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, some user not found').to_dict(), HTTPStatus.NOT_FOUND 

        return {
            'is_follower': is_follower
        }, HTTPStatus.OK


    @follows_blueprint.route('/users/follow/<target_username>', methods=['PUT'])
    @token_required
    def follow(current_user: User, target_username: str):
        username: str = current_user.username
    
        try:
            follow_service.follow(username, target_username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except SameUserException:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, some user not found').to_dict(), HTTPStatus.NOT_FOUND 
        except AlreadyFollowException:
            return Error('Already following').to_dict(), HTTPStatus.CONFLICT
        
        return {
            'message': 'successfully followed'
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/unfollow/<target_username>', methods=['PUT'])
    @token_required
    def unfollow(current_user: User, target_username: str):
        username: str = current_user.username
    
        try:
            follow_service.unfollow(username, target_username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except SameUserException:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, some user not found').to_dict(), HTTPStatus.NOT_FOUND 
        except NotFollowerException:
            return Error('Must be a follower to unfollow').to_dict(), HTTPStatus.CONFLICT
        
        return {
            'message': 'successfully unfollowed'
        }, HTTPStatus.OK

    
    @follows_blueprint.route('/users/<username>/followers', methods=['GET'])
    @token_required
    def get_user_followers(current_user: User, username: str):
        try:
            followers = follow_service.find_all_followers(username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        return {
            'username': username,
            'followers_counter': len(followers),
            'followers': [f_user.to_dict() for f_user in followers]
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/<username>/following', methods=['GET'])
    @token_required
    def get_user_following(current_user: User, username: str):
        try:
            following = follow_service.find_all_following(username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        return {
            'username': username,
            'following_counter': len(following),
            'following': [f_user.to_dict() for f_user in following]
        }, HTTPStatus.OK


    return follows_blueprint