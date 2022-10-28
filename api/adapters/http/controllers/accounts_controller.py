from http import HTTPStatus
from flask import Blueprint, request
import inject

from domain.models.User import User

from domain.services.UserService import UserService

from ..auth import create_token

@inject.autoparams()
def create_accounts_blueprint(user_service: UserService) -> Blueprint:
    accounts_blueprint = Blueprint('account', __name__)

    @accounts_blueprint.route('/register', methods=['POST'])
    def register():
        name: str = request.json.get('name')
        username: str = request.json.get('username').lower()
        password: str = request.json.get('password')

        user = user_service.create(name, username, password)

        token = create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.CREATED


    @accounts_blueprint.route('/login', methods=['POST'])
    def login():
        username: str = request.json.get('username')
        try_password: str = request.json.get('password')

        user: User = user_service.login(username, try_password)

        token = create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.OK

    return accounts_blueprint