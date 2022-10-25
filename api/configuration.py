import inject
from dotenv import load_dotenv
from flask import Flask

from domain.interfaces.IFollowerRepository import IFollowerRepository
from adapters.db.ListFollowerRepository import ListFollowerRepository

from domain.interfaces.IUserRepository import IUserRepository
from adapters.db.ListUserRepository import ListUserRepository

def configure_api(api: Flask) -> None:
    load_dotenv()

def configure_inject(api: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_constructor(IUserRepository, ListUserRepository)
        binder.bind_to_constructor(IFollowerRepository, ListFollowerRepository)
    
    inject.configure(config)