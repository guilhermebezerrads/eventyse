import inject
from dotenv import load_dotenv
from flask import Flask

from domain.interfaces.IUserRepository import IUserRepository
from adapters.db.ListUserRepository import ListUserRepository

from domain.interfaces.IUserService import IUserService
from domain.services.UserService import UserService

def configure_api(api: Flask) -> None:
    load_dotenv()

def configure_inject(api: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(IUserRepository, ListUserRepository())
        binder.bind(IUserService, UserService(ListUserRepository()))
    
    inject.configure(config)