import inject
from dotenv import load_dotenv
from flask import Flask

from domain.interfaces.IFollowRepository import IFollowRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository

from domain.interfaces.IUserRepository import IUserRepository
from adapters.db.InMemoryUserRepository import InMemoryUserRepository

def configure_api(api: Flask) -> None:
    load_dotenv()

def configure_inject(api: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_constructor(IUserRepository, InMemoryUserRepository)
        binder.bind_to_constructor(IFollowRepository, InMemoryFollowRepository)
     
    inject.configure(config)