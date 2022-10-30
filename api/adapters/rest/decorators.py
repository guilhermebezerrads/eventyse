import inject
from functools import wraps
from flask import request

from domain.ports.ITokenService import ITokenService

def token_required(f):
    @wraps(f)
    @inject.autoparams('token_service')
    def decorated(token_service: ITokenService, *args, **kwargs):
        token = request.headers.get('Token')
        current_user = token_service.authenticate_token(token)

        return f(current_user, *args, **kwargs)
    return decorated
