import inject
from dotenv import load_dotenv
from flask import Flask

from domain.ports.IUserRepository import IUserRepository
from domain.ports.IFollowRepository import IFollowRepository
from domain.ports.IRoadmapRepository import IRoadmapRepository
from domain.ports.ICommentRepository import ICommentRepository
from domain.ports.IUserService import IUserService
from domain.ports.IFollowService import IFollowService
from domain.ports.IRoadmapService import IRoadmapService
from domain.ports.ICommentService import ICommentService

from adapters.db.InMemoryUserRepository import InMemoryUserRepository
from adapters.db.InMemoryFollowRepository import InMemoryFollowRepository
from adapters.db.InMemoryRoadmapRepository import InMemoryRoadmapRepository
from adapters.db.InMemoryCommentRepository import InMemoryCommentRepository

from domain.services.UserService import UserService
from domain.services.FollowService import FollowService
from domain.services.RoadmapService import RoadmapService
from domain.services.CommentService import CommentService

def configure_api(api: Flask) -> None:
    load_dotenv()

def configure_inject(api: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_constructor(IUserRepository, InMemoryUserRepository)
        binder.bind_to_constructor(IFollowRepository, InMemoryFollowRepository)
        binder.bind_to_constructor(IRoadmapRepository, InMemoryRoadmapRepository)
        binder.bind_to_constructor(ICommentRepository, InMemoryCommentRepository)

        binder.bind_to_constructor(IUserService, UserService)
        binder.bind_to_constructor(IFollowService, FollowService)
        binder.bind_to_constructor(IRoadmapService, RoadmapService)
        binder.bind_to_constructor(ICommentService, CommentService)
     
    inject.configure(config)
