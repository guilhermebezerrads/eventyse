import inject
from sqlalchemy.orm import Session

from domain.ports.IRoadmapRepository import IRoadmapRepository
from domain.ports.IFollowRepository import IFollowRepository

from domain.models.Roadmap import Roadmap

from adapters.db.interfaces.IDatabase import IDatabase
from adapters.db import SQLAlchemy
from adapters.db.utils.mapper import *

class SQLAlchemyRoadmapRepository(IRoadmapRepository):
    @inject.autoparams()
    def __init__(self, db: IDatabase) -> None:
        self.db: IDatabase = db
        self.session: Session = db.session

    def create(self, roadmap:Roadmap) -> Roadmap:
        roadmap_db, coord_list, tag_list = roadmap_model_to_roadmap_db(roadmap)

        self.session.add(roadmap_db)
        self.session.commit()

        self.create_coordinates(roadmap.id, coord_list)
        self.create_tags(roadmap.id, tag_list)

        return roadmap_db_to_roadmap_model(roadmap_db)

    def create_coordinates(self, roadmap_id, coord_list):
        for coord in coord_list:
            coordinate = SQLAlchemy.Coordinate(lati=coord[0], long=coord[1], roadmap_id=roadmap_id)
            self.session.add(coordinate)
        self.session.commit()
        
        coordinates = self.session.query(SQLAlchemy.Coordinate).filter_by(roadmap_id = roadmap_id).all()
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()
        roadmap_db.coordinates = [coord for coord in coordinates]        
        
        self.session.commit()

    def create_tags(self, roadmap_id, tag_list):
        for tag in tag_list:
            tags_exists = self.session.query(SQLAlchemy.Tag).filter_by(name=tag).first()
            if tags_exists is None:
                tag_db = SQLAlchemy.Tag(name=tag)
                self.session.add(tag_db)

        self.session.commit()

        print(tag_list)
        tags = self.session.query(SQLAlchemy.Tag).filter(SQLAlchemy.Tag.name.in_(tag_list)).all()
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()
        roadmap_db.tags = [tag for tag in tags]

        self.session.commit()

    def find_by_id(self, roadmap_id: str) -> Roadmap:
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()
        
        if roadmap_db is None:
            return None

        return roadmap_db_to_roadmap_model(roadmap_db)

    def find_all(self) -> list[Roadmap]:
        roadmaps_db = self.session.query(SQLAlchemy.Roadmap).all()

        roadmaps = []

        for roadmap_db in roadmaps_db:
            roadmaps.append(roadmap_db_to_roadmap_model(roadmap_db))

        return roadmaps

    def find_all_by_username(self, username: str) -> list[Roadmap]:
        user_roadmaps_db = self.session.query(SQLAlchemy.Roadmap).filter_by(author_username=username).all()
        user_roadmaps: list[Roadmap] = []

        for roadmap_db in user_roadmaps_db:
            user_roadmaps.append(roadmap_db_to_roadmap_model(roadmap_db))

        return user_roadmaps

    def find_all_by_following(self, username: str) -> list[Roadmap]:
        following_roadmaps: list[Roadmap] = []

        users_following = self.session.query(SQLAlchemy.following).filter(SQLAlchemy.following.c.username==username).all()

        usernames = []
        for user in users_following:
            usernames.append(user.target_username)

        following_roadmaps_db = self.session.query(SQLAlchemy.Roadmap).filter(SQLAlchemy.Roadmap.author_username.in_(usernames)).all()

        following_roadmaps = []
        for roadmap_db in following_roadmaps_db:
            following_roadmaps.append(roadmap_db_to_roadmap_model(roadmap_db))

        return following_roadmaps

    def find_all_by_tags(self, tags: list[str]) -> list[Roadmap]:
        tags_roadmaps: list[Roadmap] = []
        tags_db = self.session.query(SQLAlchemy.tags).filter(SQLAlchemy.tags.c.tag_name.in_(tags)).all()

        roadmap_ids = []
        for tag in tags_db:
            roadmap_ids.append(tag.roadmap_id)

        roadmaps_db = self.session.query(SQLAlchemy.Roadmap).filter(SQLAlchemy.Roadmap.id.in_(roadmap_ids)).all()

        for roadmap_db in roadmaps_db:
            tags_roadmaps.append(roadmap_db_to_roadmap_model(roadmap_db))

        return tags_roadmaps

    def is_liked(self, username: str, roadmap_id: str) -> bool:
        rating = self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).first()

        if rating is not None and rating.val == True:
            return True
        
        return False

    def is_disliked(self, username: str, roadmap_id: str) -> bool:
        rating = self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).first()

        if rating is not None and rating.val == False:
            return True
        
        return False

    def add_eval(self, username: str, roadmap_id: str, eval: bool) -> None:
        evaluation = SQLAlchemy.evaluations.insert().values(username=username, roadmap_id=roadmap_id, val=eval)
        self.session.execute(evaluation)

    def add_like(self, username: str, roadmap_id: str) -> None:
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()

        if self.is_disliked(username, roadmap_id):
            self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).delete()        
            roadmap_db.dislikes -= 1
            self.add_eval(username, roadmap_id, True)
            roadmap_db.likes += 1
        else:
            self.add_eval(username, roadmap_id, True)
            roadmap_db.likes += 1

        self.session.commit()

    def add_dislike(self, username: str, roadmap_id: str) -> None:
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()

        if self.is_liked(username, roadmap_id):
            self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).delete()        
            roadmap_db.likes -= 1
            self.add_eval(username, roadmap_id, False)
            roadmap_db.dislikes += 1
        else:
            self.add_eval(username, roadmap_id, False)
            roadmap_db.dislikes += 1

        self.session.commit()

    def remove_like(self, username: str, roadmap_id: str) -> None:
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()
        self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).delete()        
        roadmap_db.likes -= 1

        self.session.commit()                

    def remove_dislike(self, username: str, roadmap_id: str) -> None:
        roadmap_db = self.session.query(SQLAlchemy.Roadmap).filter_by(id=roadmap_id).first()
        self.session.query(SQLAlchemy.evaluations).filter(SQLAlchemy.evaluations.c.username==username, SQLAlchemy.evaluations.c.roadmap_id==roadmap_id).delete()                
        roadmap_db.dislikes -= 1

        self.session.commit()
