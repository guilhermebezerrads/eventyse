from http import HTTPStatus
from flask import Blueprint
import inject

from domain.models.User import User
from domain.models.Error import Error
from domain.services.FollowService import FollowService
from domain.services.UserService import UserService

from ..auth import token_required

@inject.autoparams()
def create_follows_blueprint(user_service: UserService, follow_service: FollowService) -> Blueprint:
    follows_blueprint = Blueprint('follows', __name__)

    @follows_blueprint.route('/users/<username>/follow/<target_username>', methods=['GET'])
    @token_required
    def already_follow(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        
        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        return {
            'follows': follow_service.already_follow(username, target_username)
        }, HTTPStatus.OK


    @follows_blueprint.route('/users/<username>/follow/<target_username>', methods=['PATCH'])
    @token_required
    def follow(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST

        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        sucess = follow_service.follow(username, target_username)
        
        if not sucess:
            return Error('already following').to_dict(), HTTPStatus.CONFLICT

        return {
            'message': 'successfull follow'
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/<username>/unfollow/<target_username>', methods=['PATCH'])
    @token_required
    def unfollow(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        
        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        sucess = follow_service.unfollow(username, target_username)

        if not sucess:
            return Error('must be a follower to unfollow').to_dict(), HTTPStatus.CONFLICT
 
        return {
            'message': 'successfull unfollow'
        }, HTTPStatus.OK

    
    @follows_blueprint.route('/users/<username>/followers', methods=['GET'])
    @token_required
    def get_user_followers(username: str):
        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        followers = follow_service.find_all_followers(user.username)

        return {
            'username': user.username,
            'followers_counter': user.followers_counter,
            'followers': [f_user.to_dict() for f_user in followers]
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/<username>/following', methods=['GET'])
    @token_required
    def get_user_following(username: str):
        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        following = follow_service.find_all_following(user.username)

        return {
            'username': user.username,
            'following_counter': user.following_counter,
            'following': [f_user.to_dict() for f_user in following]
        }, HTTPStatus.OK


    return follows_blueprint