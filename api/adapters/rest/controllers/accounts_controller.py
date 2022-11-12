from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.models.User import User

from domain.ports.IUserService import IUserService
from domain.ports.ITokenService import ITokenService

@inject.autoparams()
def create_accounts_blueprint(user_service: IUserService, token_service: ITokenService) -> Blueprint:
    accounts_blueprint = Blueprint('account', __name__)

    @accounts_blueprint.route('/register', methods=['POST'])
    def register():
        name: str = request.json.get('name')
        username: str = request.json.get('username').lower()
        password: str = request.json.get('password')

        user = user_service.create(name, username, password)

        token = token_service.create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.CREATED


    @accounts_blueprint.route('/login', methods=['POST'])
    def login():
        username: str = request.json.get('username')
        try_password: str = request.json.get('password')

        user: User = user_service.login(username, try_password)

        token = token_service.create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.OK

    return accounts_blueprint