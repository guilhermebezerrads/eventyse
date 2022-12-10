import inject
import jwt, os, datetime

from domain.exceptions.TokenException import TokenException

from domain.ports.ITokenService import ITokenService
from domain.ports.IUserRepository import IUserRepository

from domain.models.User import User

class TokenService(ITokenService):
    @inject.autoparams()
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    

    def authenticate_token(self, token: str):
        if not token:
            raise TokenException('authentication token is missing')
        
        try:
            data = jwt.decode(
                token, 
                os.environ.get('SECRET_KEY'),
                algorithms="HS256"
            )
            current_user = self.user_repository.find_by_username(data['username'])
            if not current_user:
                raise TokenException('invalid authentication token')
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenException('authentication token expired')
        
        return current_user
    

    def create_token(self, user: User):
        env_key = os.environ.get('SECRET_KEY')
        token = jwt.encode(
            {
                'username': user.username,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=24),
            },
            env_key,
            algorithm="HS256"
        )
        return token
