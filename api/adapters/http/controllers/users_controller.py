from http import HTTPStatus
from flask import Blueprint
import inject

from domain.models.User import User
from domain.models.Error import Error
from domain.interfaces.IUserService import IUserService

from ..auth import token_required

users_blueprint = Blueprint('users', __name__)

@inject.autoparams()
def create_users_blueprint(user_service: IUserService) -> Blueprint:
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
    
    return users_blueprint
