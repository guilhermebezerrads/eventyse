from injector import singleton

from adapters.db.ListUserRepository import ListUserRepository
from domain.ports.IUserRepository import IUserRepository

from domain.services.UserService import UserService

def configure(binder):
    binder.bind(IUserRepository, to=ListUserRepository, scope=singleton)
    binder.bind(UserService, to=UserService, scope=singleton)
