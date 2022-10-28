from http import HTTPStatus
from flask import Blueprint

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.UsernameAlreadyExistsException import UsernameAlreadyExistsException
from domain.exceptions.UnauthorizedException import UnauthorizedException
from domain.exceptions.AlreadyFollowException import AlreadyFollowException
from domain.exceptions.AlreadyLikedException import AlreadyLikedException
from domain.exceptions.NotFollowerException import NotFollowerException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.NotLikedException import NotLikedException
from domain.exceptions.SameUserException import SameUserException
from domain.exceptions.AlreadyDislikedException import AlreadyDislikedException
from domain.exceptions.NotDislikedException import NotDislikedException
from domain.exceptions.TokenException import TokenException

def create_exceptions_blueprint() -> Blueprint:
    exceptions_blueprint = Blueprint('exceptions', __name__)

    @exceptions_blueprint.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_internal_server_error(error):
        return {
            'message': 'something went wrong on the server '
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @exceptions_blueprint.app_errorhandler(TokenException)
    def handle_token_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.UNAUTHORIZED

    @exceptions_blueprint.app_errorhandler(MissingFieldException)
    def handle_missing_field_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.BAD_REQUEST

    @exceptions_blueprint.app_errorhandler(UsernameAlreadyExistsException)
    def handle_username_already_exists_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.CONFLICT
    
    @exceptions_blueprint.app_errorhandler(NotFoundException)
    def handle_not_found_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.NOT_FOUND
    
    @exceptions_blueprint.app_errorhandler(UnauthorizedException)
    def handle_unauthorizaed_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.UNAUTHORIZED

    @exceptions_blueprint.app_errorhandler(SameUserException)
    def handle_same_user_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.BAD_REQUEST
    
    @exceptions_blueprint.app_errorhandler(AlreadyFollowException)
    def handle_already_follow_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.CONFLICT
    	
    @exceptions_blueprint.app_errorhandler(NotFollowerException)
    def handle_not_follower_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.BAD_REQUEST

    @exceptions_blueprint.app_errorhandler(AlreadyLikedException)
    def handle_already_liked_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.CONFLICT

    @exceptions_blueprint.app_errorhandler(NotLikedException)
    def handle_not_liked_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.BAD_REQUEST
    
    @exceptions_blueprint.app_errorhandler(AlreadyDislikedException)
    def handle_already_disliked_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.CONFLICT
    
    @exceptions_blueprint.app_errorhandler(NotDislikedException)
    def handle_not_disliked_exception(error):
        return {
            'message': str(error)
        }, HTTPStatus.BAD_REQUEST

    return exceptions_blueprint
