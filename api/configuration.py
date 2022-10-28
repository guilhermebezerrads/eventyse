import inject
from dotenv import load_dotenv
from flask import Flask

from domain.interfaces.IUserRepository import IUserRepository
from adapters.db.InMemoryUserRepository import InMemoryUserRepository

from domain.interfaces.IFollowRepository import IFollowRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository

from domain.interfaces.IRoadmapRepository import IRoadmapRepository
from adapters.db.InMemoryRoadmapRepository import InMemoryRoadmapRepository

from domain.interfaces.ICommentRepository import ICommentRepository
from adapters.db.InMemoryCommentRepository import InMemoryCommentRepository

def configure_api(api: Flask) -> None:
    load_dotenv()

def configure_inject(api: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_constructor(IUserRepository, InMemoryUserRepository)
        binder.bind_to_constructor(IFollowRepository, InMemoryFollowRepository)
        binder.bind_to_constructor(IRoadmapRepository, InMemoryRoadmapRepository)
        binder.bind_to_constructor(ICommentRepository, InMemoryCommentRepository)
     
    inject.configure(config)
