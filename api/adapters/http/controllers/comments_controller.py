from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.NotFoundException import NotFoundException

from domain.models.Comment import Comment
from domain.models.User import User
from domain.models.Error import Error

from domain.services.CommentService import CommentService

from ..auth import token_required

@inject.autoparams()
def create_comment_blueprint(comment_service: CommentService) -> Blueprint:
    comments_blueprint = Blueprint('comments', __name__)

    @comments_blueprint.route('/comments/<roadmap_id>', methods=['GET'])
    @token_required
    def get_comments_by_roadmap_id(current_user: User, roadmap_id: str):
        try:
            roadmap_comments: list[Comment] = comment_service.find_all_by_roadmap_id(roadmap_id)
        except MissingFieldException:
            return Error('error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('error, roadmap not found').to_dict(), HTTPStatus.NOT_FOUND

        return [roadmap.to_dict() for roadmap in roadmap_comments], HTTPStatus.OK
    
    
    @comments_blueprint.route('/comments/<roadmap_id>', methods=['POST'])
    @token_required
    def create_comment(current_user: User, roadmap_id: str):
        username: str = current_user.username
        text: str = request.json.get('text')

        try:
            comment: Comment = comment_service.create(username, roadmap_id, text)
        except MissingFieldException:
            return Error('error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('error, roadmap not found').to_dict(), HTTPStatus.NOT_FOUND 

        return comment.to_dict(), HTTPStatus.OK


    return comments_blueprint
