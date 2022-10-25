import datetime
from http import HTTPStatus
import jwt
import os
import bcrypt
from functools import wraps
from flask import request

# from injector import inject
import inject

from domain.entities.User import User
from domain.entities.Error import Error

from domain.interfaces.IUserService import IUserService

def token_required(f):
    @wraps(f)
    @inject.autoparams('user_service')
    def decorated(user_service: IUserService, *args, **kwargs):
        token = None
        if 'Token' in request.headers.keys():
            token = request.headers['Token']
        if not token:
            return Error('authentication token is missing').to_dict(), HTTPStatus.UNAUTHORIZED
        try:
            data = jwt.decode(
                token, 
                os.environ.get('SECRET_KEY'),
                algorithms="HS256"
            )
            current_user = user_service.find_by_username(data['username'])
            if not current_user:
                return Error("invalid authentication token").to_dict(), HTTPStatus.UNAUTHORIZED
        except:
            return Error('something went wrong').to_dict(), HTTPStatus.INTERNAL_SERVER_ERROR
        return f(*args, **kwargs)
    return decorated


def check_password_hash(user: User, try_password: str):
    try_password_hash = bcrypt.hashpw(try_password.encode(), user.password_salt.encode())
    return try_password_hash.decode() == user.password_hash


def create_token(user: User):
    token = jwt.encode(
        {
            'username': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24),
        },
        os.environ.get('SECRET_KEY'),
        algorithm="HS256"
    )
    return token