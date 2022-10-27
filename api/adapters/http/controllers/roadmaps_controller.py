from email.policy import HTTP
from http import HTTPStatus
from lib2to3.pgen2 import token
from flask import Blueprint, request
import inject

from domain.models.Roadmap import Roadmap, roadmap_factory
from domain.models.Error import Error
from domain.services.RoadmapService import RoadmapService

from ..auth import token_required

@inject.autoparams()
def create_roadmaps_blueprint(roadmap_service: RoadmapService) -> Blueprint:
    roadmaps_blueprint = Blueprint('roadmaps', __name__)

    @roadmaps_blueprint.route('/roadmaps', methods=['GET'])
    @token_required
    def get_all():
        roadmaps: list[Roadmap] = roadmap_service.find_all()

        return [roadmap.to_dict() for roadmap in roadmaps], HTTPStatus.OK
    
    
    @roadmaps_blueprint.route('/roadmaps/<roadmap_id>', methods=['GET'])
    @token_required
    def get_all_by_roadmap_id(roadmap_id: str):
        roadmap: Roadmap = roadmap_service.find_by_id(roadmap_id)

        if not roadmap:
            return Error('Error, roadmap not found').to_dict(), HTTPStatus.NOT_FOUND 

        return roadmap.to_dict(), HTTPStatus.OK

    @roadmaps_blueprint.route('/roadmaps', methods=['POST'])
    @token_required
    def add_roadmap():
        username: str = request.json['username']
        title: str = request.json['title']
        description: str = request.json['description']
        coordinates: list[list[float]] = request.json['coordinates']
        tags: list[str] = request.json['tags']

        roadmap: Roadmap = roadmap_factory(username, title, description, coordinates, tags)

        if roadmap_service.add(roadmap):
            return roadmap.to_dict(), HTTPStatus.CREATED
    
    @roadmaps_blueprint.route('/roadmaps/like', methods=['PATCH'])
    @token_required
    def like_roadmap():
        username: str = request.json['username']
        roadmap_id: str = request.json['roadmapId']

        success = roadmap_service.like(username, roadmap_id)

        if not success:
            return Error('already liked').to_dict(), HTTPStatus.CONFLICT

        return {
            'message': 'successfully liked'
        }, HTTPStatus.OK
    
    @roadmaps_blueprint.route('/roadmaps/deslike', methods=['PATCH'])
    @token_required
    def deslike_roadmap():
        username: str = request.json['username']
        roadmap_id: str = request.json['roadmapId']

        success = roadmap_service.deslike(username, roadmap_id)

        if not success:
            return Error('already desliked').to_dict(), HTTPStatus.CONFLICT

        return {
            'message': 'successfully desliked'
        }, HTTPStatus.OK

    @roadmaps_blueprint.route('/roadmaps/following', methods=['GET'])
    @token_required
    def get_all_by_following():
        username: str = request.json['username']

        following_roadmaps: list[Roadmap] = roadmap_service.find_all_by_following(username)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in following_roadmaps]
        }, HTTPStatus.OK

    @roadmaps_blueprint.route('/roadmaps/user', methods=['GET'])
    @token_required
    def get_all_by_username():
        username: str = request.json['username']

        user_roadmaps: list[Roadmap] = roadmap_service.find_all_by_username(username)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in user_roadmaps]
        }, HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/tags', methods=['GET'])
    @token_required
    def get_all_by_tags():
        tags: list[str] = request.json['tags']

        tags_roadmaps: list[Roadmap] = roadmap_service.find_all_by_tags(tags)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in tags_roadmaps]
        }, HTTPStatus.OK

    
    return roadmaps_blueprint
