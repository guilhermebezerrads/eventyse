import inject
from sqlalchemy.orm import Session

from domain.ports.ICommentRepository import ICommentRepository
from domain.models.Comment import Comment

from adapters.db.interfaces.IDatabase import IDatabase
from adapters.db import SQLAlchemy
from adapters.db.utils.mapper import *

class SQLAlchemyCommentRepository(ICommentRepository):
    @inject.autoparams()
    def __init__(self, db: IDatabase) -> None:
        self.db: IDatabase = db
        self.session: Session = db.session

    def create(self, comment: Comment) -> Comment:
        comment_db = comment_model_to_comment_db(comment)
        self.session.add(comment_db)
        self.session.commit()

        return comment

    def find_by_id(self, comment_id: str) -> Comment:
        comment_db = self.session.query(SQLAlchemy.Comment).filter_by(id=comment_id).first()

        if comment_db:
            return comment_db_to_comment_model(comment_db)

        return None

    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        roadmap_comments_db = self.session.query(SQLAlchemy.Comment).filter_by(roadmap_id=roadmap_id).all()
        roadmap_comments: list[Comment] = []

        for comment in roadmap_comments_db:
            roadmap_comments.append(comment_db_to_comment_model(comment))

        return roadmap_comments
    
    def delete_by_id(self, comment_id: str) -> None:
        self.session.query(SQLAlchemy.Comment).filter_by(id=comment_id).delete()
        self.session.commit()
    
