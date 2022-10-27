from http import HTTPStatus
from msilib.schema import Error
from flask import Blueprint, request, Response
import inject
import bcrypt

from domain.models.User import User, user_factory
from domain.models.Error import Error
from domain.services.UserService import UserService

from ..auth import create_token, check_password_hash

@inject.autoparams()
def create_accounts_blueprint(user_service: UserService) -> Blueprint:
    accounts_blueprint = Blueprint('account', __name__)

    @accounts_blueprint.route('/register', methods=['POST'])
    def register() -> Response:
        name: str = request.json['name']
        username: str = request.json['username'].lower()
        password: bytes = str.encode(request.json['password'])

        password_salt: bytes = bcrypt.gensalt()
        password_hash: bytes = bcrypt.hashpw(password, password_salt)
        
        if user_service.already_exists(username):
            return Error('Error, username already taken').to_dict(), HTTPStatus.CONFLICT

        user = user_factory(name, username, password_hash, password_salt)

        user_service.add(user)

        token = create_token(user)

        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.CREATED


    @accounts_blueprint.route('/login', methods=['POST'])
    def login() -> Response:
        username: str = request.json['username']
        try_password: str = request.json['password']

        user: User = user_service.find_by_username(username)

        if not user:
            return Error('Error, invalid username').to_dict(), HTTPStatus.NOT_FOUND
        
        if not check_password_hash(user, try_password):
            return Error('Error, invalid password').to_dict(), HTTPStatus.UNAUTHORIZED

        token = create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.OK

    return accounts_blueprint