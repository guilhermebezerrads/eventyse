from http import HTTPStatus
from flask import Blueprint
import inject

from domain.models.User import User
from domain.models.Error import Error
from domain.services.FollowerService import FollowerService
from domain.services.UserService import UserService

from ..auth import token_required

users_blueprint = Blueprint('users', __name__)

@inject.autoparams()
def create_users_blueprint(user_service: UserService, follower_service: FollowerService) -> Blueprint:
    users_blueprint = Blueprint('users', __name__)

    @users_blueprint.route('/users', methods=['GET'])
    @token_required
    def get_users():
        users: list[User] = user_service.find_all()
        return [user.to_dict() for user in users], HTTPStatus.OK


    @users_blueprint.route('/users/<username>', methods=['GET'])
    @token_required
    def get_user(username: str):
        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        return user.to_dict(), HTTPStatus.OK
    

    @users_blueprint.route('/users/<username>/follows/<target_username>', methods=['GET'])
    @token_required
    def check_if_follows(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        
        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        return {
            'follows': follower_service.already_follow(username, target_username)
        }


    @users_blueprint.route('/users/<username>/follows/<target_username>', methods=['PUT'])
    @token_required
    def add_follows(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST

        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        follower_service.add_follow(username, target_username)

        return '', HTTPStatus.NO_CONTENT
    

    @users_blueprint.route('/users/<username>/follows/<target_username>', methods=['DELETE'])
    @token_required
    def remove_follows(username: str, target_username: str):
        if username == target_username:
            return Error('Error, usernames must be different').to_dict(), HTTPStatus.BAD_REQUEST
        
        user: User = user_service.find_by_username(username)
        user_target: User = user_service.find_by_username(target_username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND

        if not user_target:
            return Error('Error, target username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        follower_service.remove_follow(username, target_username)
        
        return '', HTTPStatus.NO_CONTENT

    
    @users_blueprint.route('/users/<username>/followers', methods=['GET'])
    @token_required
    def get_user_followers(username: str):
        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        followers = follower_service.find_all_followers(user.username)

        return {
            'username': user.username,
            'followers_counter': user.followers_counter,
            'followers': followers
        }, HTTPStatus.OK
    
    @users_blueprint.route('/users/<username>/following', methods=['GET'])
    @token_required
    def get_user_following(username: str):
        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, username not found').to_dict(), HTTPStatus.NOT_FOUND
        
        following = follower_service.find_all_following(user.username)

        return {
            'username': user.username,
            'following_counter': user.following_counter,
            'following': following
        }, HTTPStatus.OK


    return users_blueprint
