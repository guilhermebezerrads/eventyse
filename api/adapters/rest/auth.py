import jwt
import os
import inject
import datetime
from functools import wraps
from flask import request

from domain.exceptions.TokenException import TokenException

from domain.models.User import User

from domain.ports.IUserRepository import IUserRepository

def token_required(f):
    @wraps(f)
    @inject.autoparams('user_repository')
    def decorated(user_repository: IUserRepository, *args, **kwargs):
        token = None
        if 'Token' in request.headers.keys():
            token = request.headers['Token']
        if not token:
            raise TokenException('authentication token is missing')
        try:
            data = jwt.decode(
                token, 
                os.environ.get('SECRET_KEY'),
                algorithms="HS256"
            )
            current_user = user_repository.find_by_username(data['username'])
            if not current_user:
                raise TokenException('invalid authentication token')
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenException('authentication token expired')
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
