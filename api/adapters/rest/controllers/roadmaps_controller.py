from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.models.Roadmap import Roadmap
from domain.models.User import User

from domain.ports.IRoadmapService import IRoadmapService

from adapters.rest.decorators import token_required

@inject.autoparams()
def create_roadmaps_blueprint(roadmap_service: IRoadmapService) -> Blueprint:
    roadmaps_blueprint = Blueprint('roadmaps', __name__)

    @roadmaps_blueprint.route('/roadmaps', methods=['POST'])
    @token_required
    def create_roadmap(current_user: User):
        username: str = current_user.username
        title: str = request.json.get('title')
        description: str = request.json.get('description')
        coordinates: list[list[float]] = request.json.get('coordinates')
        tags: list[str] = request.json.get('tags')

        roadmap = roadmap_service.create(username, title, description, coordinates, tags)

        return roadmap.to_dict(), HTTPStatus.CREATED


    @roadmaps_blueprint.route('/roadmaps', methods=['GET'])
    @token_required
    def get_roadmaps(current_user: User):
        roadmaps: list[Roadmap] = roadmap_service.find_all()
        return [roadmap.to_dict() for roadmap in roadmaps], HTTPStatus.OK
    
    
    @roadmaps_blueprint.route('/roadmaps/<roadmap_id>', methods=['GET'])
    @token_required
    def get_roadmap_by_id(current_user: User, roadmap_id: str):
        roadmap: Roadmap = roadmap_service.find_by_id(roadmap_id)

        return roadmap.to_dict(), HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/user/<username>', methods=['GET'])
    @token_required
    def get_roadmap_by_username(current_user: User, username: str):
        user_roadmaps: list[Roadmap] = roadmap_service.find_all_by_username(username)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in user_roadmaps]
        }, HTTPStatus.OK
    

    @roadmaps_blueprint.route('/roadmaps/following', methods=['GET'])
    @token_required
    def get_roadmap_by_following(current_user: User):
        username: str = current_user.username

        following_roadmaps: list[Roadmap] = roadmap_service.find_all_by_following(username)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in following_roadmaps]
        }, HTTPStatus.OK


    @roadmaps_blueprint.route('/roadmaps/tags', methods=['GET'])
    @token_required
    def get_roadmaps_by_tags(current_user: User):
        tags: list[str] = request.json.get('tags')

        tags_roadmaps: list[Roadmap] = roadmap_service.find_all_by_tags(tags)

        return {
            'roadmaps': [roadmap.to_dict() for roadmap in tags_roadmaps]
        }, HTTPStatus.OK
    

    return roadmaps_blueprint
