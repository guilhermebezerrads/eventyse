from csv import excel_tab
from http import HTTPStatus
from msilib.schema import Error
from flask import Blueprint, request
import inject

from domain.exceptions.MissingFieldException import MissingFieldException
from domain.exceptions.UsernameAlreadyExistsException import UsernameAlreadyExistsException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException

from domain.models.User import User
from domain.models.Error import Error

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

        try:
            user = user_service.create(name, username, password)
        except MissingFieldException:
            return Error('error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except UsernameAlreadyExistsException:
            return Error('error, username already taken').to_dict(), HTTPStatus.CONFLICT 

        token = create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.CREATED


    @accounts_blueprint.route('/login', methods=['POST'])
    def login():
        username: str = request.json.get('username')
        try_password: str = request.json.get('password')

        try:
            user: User = user_service.login(username, try_password)
        except MissingFieldException:
            return Error('error, missing field').to_dict(), HTTPStatus.BAD_REQUEST
        except NotFoundException:
            return Error('error, invalid username').to_dict(), HTTPStatus.NOT_FOUND
        except UnauthorizedException:
            return Error('error, invalid password').to_dict(), HTTPStatus.UNAUTHORIZED

        token = create_token(user)
        
        return {
            'username': user.username,
            'token': token
        }, HTTPStatus.OK

    return accounts_blueprint