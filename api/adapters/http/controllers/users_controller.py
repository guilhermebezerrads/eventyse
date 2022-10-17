from flask import Blueprint, request
from injector import inject

from domain.entities.User import User
from domain.ports.IUserService import IUserService

app_users = Blueprint('app_users', __name__)

@inject
@app_users.route('/users', methods=['GET'])
def get_users(user_service: IUserService):
    return [user.__dict__ for user in user_service.find_all()]

@inject
@app_users.route('/users/<username>', methods=['GET'])
def get_user(username: str, user_service: IUserService):
    user: User = user_service.find_by_username(username)

    if user == None:
        return {
            'message': 'Error, username not found'
        }, 404
    
    return user.__dict__, 200
