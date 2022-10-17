from flask import Blueprint, request
from injector import inject

from domain.entities.User import User
from domain.services.UserService import UserService

app_account = Blueprint('app_account', __name__)

@inject
@app_account.route('/register', methods=['POST'])
def register(user_service: UserService):
    name = request.json['name']
    username = request.json['username']

    if user_service.already_existis(username):
        return {
            'message': 'Error, username already taken'
        }

    user = User(name, username)

    user_service.add(user)
    return user.__dict__, 201
