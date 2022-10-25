from http import HTTPStatus
from msilib.schema import Error
from flask import Blueprint, request, Response
import inject
import bcrypt
from domain.entities.Post import Post

from domain.entities.User import User
from domain.entities.Error import Error
from domain.interfaces.IUserService import IUserService

from ..auth import create_token, check_password_hash

@inject.autoparams()
def create_account_blueprint(user_service: IUserService) -> Blueprint:
    account_blueprint = Blueprint('account', __name__)

    @account_blueprint.route('/register', methods=['POST'])
    def register() -> Response:
        name: str = request.json['name']
        username: str = request.json['username'].lower()
        password: bytes = str.encode(request.json['password'])

        password_salt: bytes = bcrypt.gensalt()
        password_hash: bytes = bcrypt.hashpw(password, password_salt)
        
        if user_service.already_exists(username):
            return Error('Error, username already taken').to_dict(), HTTPStatus.BAD_REQUEST

        post1 = Post('Titulo um')
        post2 = Post('Titulo dois')

        user = User(name, username, password_hash=password_hash.decode(), password_salt=password_salt.decode(), posts=[post1, post2])

        user_service.add(user)

        token = create_token(user)

        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.CREATED


    @account_blueprint.route('/login', methods=['POST'])
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

    return account_blueprint