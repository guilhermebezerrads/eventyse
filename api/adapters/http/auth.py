import jwt
import os
import inject
import datetime
from functools import wraps
from flask import request
from http import HTTPStatus

from domain.models.User import User
from domain.models.Error import Error
from domain.services.UserService import UserService

def token_required(f):
    @wraps(f)
    @inject.autoparams('user_service')
    def decorated(user_service: UserService, *args, **kwargs):
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
        except jwt.exceptions.ExpiredSignatureError:
            return Error("authentication token expired").to_dict(), HTTPStatus.UNAUTHORIZED
        except:
            return Error('something went wrong').to_dict(), HTTPStatus.INTERNAL_SERVER_ERROR
        return f(current_user, *args, **kwargs)
    return decorated

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