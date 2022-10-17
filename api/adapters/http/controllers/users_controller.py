from flask import Blueprint, request
from injector import inject

from domain.entities.User import User
from domain.services.UserService import UserService

app_users = Blueprint('app_users', __name__)

@inject
@app_users.route('/users', methods=['GET'])
def get_users(user_service: UserService):
    return [user.__dict__ for user in user_service.find_all()]

@inject
@app_users.route('/users/<username>', methods=['GET'])
def get_user(username: str, user_service: UserService):
    user = user_service.find_by_username(username)

    if user == None:
        return {
            'message': 'Error, username not found'
        }, 404
    
    return user.__dict__, 200

# @inject
# @app_users.route('/users', methods=['POST'])
# def create_user(user_service: UserService):
#     name = request.json['name']
#     username = request.json['username']

#     if user_service.already_existis(username):
#         return {
#             'message': 'Error, username already taken'
#         }

#     user = User(name, username)

#     user_service.add(user)
#     return user.__dict__, 201
