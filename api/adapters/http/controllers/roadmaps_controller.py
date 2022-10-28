from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.AlreadyDislikedException import AlreadyDislikedException
from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.models.Roadmap import Roadmap
from domain.models.User import User
from domain.models.Error import Error

from domain.services.RoadmapService import RoadmapService
from domain.services.UserService import UserService

from ..auth import token_required

@inject.autoparams()
def create_roadmaps_blueprint(roadmap_service: RoadmapService) -> Blueprint:
    roadmaps_blueprint = Blueprint('roadmaps', __name__)

    @roadmaps_blueprint.route('/roadmaps', methods=['GET'])
    @token_required
    def get_roadmaps(current_user: User):
        roadmaps: list[Roadmap] = roadmap_service.find_all()
        return [roadmap.to_dict() for roadmap in roadmaps], HTTPStatus.OK
    
    
    @roadmaps_blueprint.route('/roadmaps/<roadmap_id>', methods=['GET'])
    @token_required
    def get_roadmap_by_id(current_user: User, roadmap_id: str):
        try:
            roadmap: Roadmap = roadmap_service.find_by_id(roadmap_id)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, roadmap not found').to_dict(), HTTPStatus.NOT_FOUND 

        return roadmap.to_dict(), HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/user/<username>', methods=['GET'])
    @token_required
    def get_roadmap_by_username(current_user: User, username: str):
        try:
            user_roadmaps: list[Roadmap] = roadmap_service.find_all_by_username(username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, user not found').to_dict(), HTTPStatus.NOT_FOUND 

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in user_roadmaps]
        }, HTTPStatus.OK
    

    @roadmaps_blueprint.route('/roadmaps/following', methods=['GET'])
    @token_required
    def get_roadmap_by_following(current_user: User):
        username: str = current_user.username

        try:
            following_roadmaps: list[Roadmap] = roadmap_service.find_all_by_following(username)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, user not found').to_dict(), HTTPStatus.NOT_FOUND

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in following_roadmaps]
        }, HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/tags', methods=['GET'])
    @token_required
    def get_roadmaps_by_tags(current_user: User):
        tags: list[str] = request.json.get('tags')

        try:
            tags_roadmaps: list[Roadmap] = roadmap_service.find_all_by_tags(tags)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in tags_roadmaps]
        }, HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps', methods=['POST'])
    @token_required
    def create_roadmap(current_user: User):
        username: str = current_user.username
        title: str = request.json.get('title')
        description: str = request.json.get('description')
        coordinates: list[list[float]] = request.json.get('coordinates')
        tags: list[str] = request.json.get('tags')

        try:
            roadmap = roadmap_service.create(username, title, description, coordinates, tags)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('Error, user not found').to_dict(), HTTPStatus.NOT_FOUND

        return roadmap.to_dict(), HTTPStatus.CREATED

    
    @roadmaps_blueprint.route('/roadmaps/like/<roadmap_id>', methods=['GET'])
    @token_required
    def is_liked(current_user: User, roadmap_id: str):
        username: str = current_user.username

        try:
            roadmap_service.is_liked(username, roadmap_id)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST 
        except NotFoundException:
            return Error('Roadmap or user not found').to_dict(), HTTPStatus.NOT_FOUND
        
        return {
            'isLiked': is_liked
        }, HTTPStatus.OK
    

    @roadmaps_blueprint.route('/roadmaps/like/<roadmap_id>', methods=['PUT'])
    @token_required
    def like_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username

        try:
            roadmap_service.like(username, roadmap_id)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST 
        except NotFoundException:
            return Error('Roadmap or user not found').to_dict(), HTTPStatus.NOT_FOUND
        except AlreadyLikedException:
            return Error('Roadmap already liked').to_dict(), HTTPStatus.CONFLICT
        
        return {
            'message': 'successfully liked'
        }, HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/dislike/<roadmap_id>', methods=['GET'])
    @token_required
    def is_disliked(current_user: User, roadmap_id: str):
        username: str = current_user.username

        try:
            is_disliked = roadmap_service.dislike(username, roadmap_id)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST 
        except NotFoundException:
            return Error('Roadmap or user not found').to_dict(), HTTPStatus.NOT_FOUND
        
        return {
            'isDisliked': is_disliked
        }, HTTPStatus.OK

    
    @roadmaps_blueprint.route('/roadmaps/dislike/<roadmap_id>', methods=['PUT'])
    @token_required
    def dislike_roadmap(current_user: User, roadmap_id: str):
        username: str = current_user.username

        try:
            roadmap_service.dislike(username, roadmap_id)
        except MissingFieldException:
            return Error('Error, missing field').to_dict(), HTTPStatus.BAD_REQUEST 
        except NotFoundException:
            return Error('Roadmap or user not found').to_dict(), HTTPStatus.NOT_FOUND
        except AlreadyDislikedException:
            return Error('Roadmap already disliked').to_dict(), HTTPStatus.CONFLICT
        
        return {
            'message': 'successfully disliked'
        }, HTTPStatus.OK

    
    return roadmaps_blueprint
