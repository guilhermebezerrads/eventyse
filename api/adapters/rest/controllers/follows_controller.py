from http import HTTPStatus
from flask import Blueprint
import inject

from domain.models.User import User

from domain.ports.IUserService import IUserService
from domain.ports.IFollowService import IFollowService

from adapters.rest.decorators import token_required

@inject.autoparams()
def create_follows_blueprint(user_service: IUserService, follow_service: IFollowService) -> Blueprint:
    follows_blueprint = Blueprint('follows', __name__)

    @follows_blueprint.route('/users/follow/<target_username>', methods=['GET'])
    @token_required
    def is_follower(current_user: User, target_username: str):
        username: str = current_user.username

        is_follower = follow_service.is_follower(username, target_username)

        return {
            'isFollower': is_follower
        }, HTTPStatus.OK


    @follows_blueprint.route('/users/follow/<target_username>', methods=['PUT'])
    @token_required
    def follow(current_user: User, target_username: str):
        username: str = current_user.username
    
        follow_service.follow(username, target_username)
        
        return {
            'message': 'successfully followed'
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/unfollow/<target_username>', methods=['PUT'])
    @token_required
    def unfollow(current_user: User, target_username: str):
        username: str = current_user.username
    
        follow_service.unfollow(username, target_username)
        
        return {
            'message': 'successfully unfollowed'
        }, HTTPStatus.OK

    
    @follows_blueprint.route('/users/<username>/followers', methods=['GET'])
    @token_required
    def get_user_followers(current_user: User, username: str):
        followers = follow_service.find_all_followers(username)

        return {
            'username': username,
            'followersCounter': len(followers),
            'followers': [f_user.to_dict() for f_user in followers]
        }, HTTPStatus.OK
    

    @follows_blueprint.route('/users/<username>/following', methods=['GET'])
    @token_required
    def get_user_following(current_user: User, username: str):
        following = follow_service.find_all_following(username)

        return {
            'username': username,
            'followingCounter': len(following),
            'following': [f_user.to_dict() for f_user in following]
        }, HTTPStatus.OK


    return follows_blueprint
