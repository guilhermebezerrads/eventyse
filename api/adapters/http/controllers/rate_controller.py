from http import HTTPStatus
from flask import Blueprint
import inject

from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.AlreadyDislikedException import AlreadyDislikedException
from domain.exceptions.NotLikedException import NotLikedException
from domain.exceptions.NotDislikedException import NotDislikedException
from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.models.User import User

from domain.services.RoadmapService import RoadmapService

from ..auth import token_required

@inject.autoparams()
def create_rates_blueprint(roadmap_service: RoadmapService) -> Blueprint:
    rates_blueprint = Blueprint('rates', __name__)
    
    @rates_blueprint.route('/roadmaps/like/<roadmap_id>', methods=['GET'])
    @token_required
    def is_roadmap_liked(current_user: User, roadmap_id: str):
        username: str = current_user.username

        is_liked = roadmap_service.is_liked(username, roadmap_id)
        
        return {
            'isLiked': is_liked
        }, HTTPStatus.OK
    

    @rates_blueprint.route('/roadmaps/like/<roadmap_id>', methods=['PUT'])
    @token_required
    def add_like_in_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username
        
        roadmap_service.add_like(username, roadmap_id)
        
        return {
            'message': 'successfully liked'
        }, HTTPStatus.OK


    @rates_blueprint.route('/roadmaps/like/<roadmap_id>', methods=['DELETE'])
    @token_required
    def remove_like_in_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username

        roadmap_service.remove_like(username, roadmap_id)
   
        return {
            'message': 'like successfully removed'
        }, HTTPStatus.OK


    @rates_blueprint.route('/roadmaps/dislike/<roadmap_id>', methods=['GET'])
    @token_required
    def is_roadmap_disliked(current_user: User, roadmap_id: str):
        username: str = current_user.username

        is_disliked = roadmap_service.is_disliked(username, roadmap_id)
        
        return {
            'isDisliked': is_disliked
        }, HTTPStatus.OK

    
    @rates_blueprint.route('/roadmaps/dislike/<roadmap_id>', methods=['PUT'])
    @token_required
    def add_dislike_in_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username

        roadmap_service.add_dislike(username, roadmap_id)
        
        return {
            'message': 'successfully disliked'
        }, HTTPStatus.OK

    
    @rates_blueprint.route('/roadmaps/dislike/<roadmap_id>', methods=['DELETE'])
    @token_required
    def remove_dislike_in_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username

        roadmap_service.remove_dislike(username, roadmap_id)
        
        return {
            'message': 'dislike successfully removed'
        }, HTTPStatus.OK

    
    return rates_blueprint
