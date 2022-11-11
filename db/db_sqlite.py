# from sqlalchemy import String, Float, Integer, ForeignKey, create_engine, Column, DateTime, Boolean, Table
# from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Base = declarative_base()

# followers = Table(
#             'following',
#             Base.metadata,
#             Column('username', ForeignKey('user.username'), nullable=False),
#             Column('target_username', ForeignKey('user.username'), nullable=False)
#         )

# evaluations = Table(
#             'evaluation',
#             Base.metadata,
#             Column('username', ForeignKey('user.username'), nullable=False),
#             Column('roadmap_id', ForeignKey('roadmap.id'), nullable=False),
#             Column('val', Boolean, nullable=False)
#         )

# class User(Base):
#     __tablename__ = "user"
#     id = Column(String, primary_key=True)
#     name = Column(String, nullable=False)
#     username = Column(String, unique=True, nullable=False)
#     password_hash = Column(String, nullable=False)
#     password_salt = Column(String, nullable=False)
#     followers_counter = Column(Integer, nullable=False)
#     following_counter = Column(Integer, nullable=False)

#     roadmaps = relationship("Roadmap")
#     following = relationship(
#         'User',
#         secondary=followers,
#         primaryjoin=followers.c.username == username,
#         secondaryjoin=followers.c.target_username == username,
#     )

# tags = Table(
#     'tags',
#     Base.metadata,
#     Column('tag_name', ForeignKey('tag.name'), nullable=False),
#     Column('roadmap_id', ForeignKey('roadmap.id'), nullable=False)
# )

# class Roadmap(Base):
#     __tablename__ = "roadmap"
#     id = Column(String, primary_key=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     created_date = Column(DateTime, nullable=False)
#     likes = Column(Integer, nullable=False)
#     dislikes = Column(Integer, nullable=False) 
#     author_username = Column(String, ForeignKey('user.username'), nullable=False)

#     coordinates = relationship("Coordinate")

#     tags = relationship('Tag', secondary=tags)                           
#     evaluations = relationship('User', secondary=evaluations)

# class Comment(Base):
#     __tablename__ = "comment"
#     id = Column(String, primary_key=True)
#     text = Column(String, nullable=False)
#     author_username = Column(String, ForeignKey('user.username'), nullable=False)
#     roadmap_id = Column(String, ForeignKey('roadmap.id'), nullable=False)
#     created_date = Column(DateTime, nullable=False)

# class Coordinate(Base):
#     __tablename__ = 'coordinate'
#     id = Column(String, primary_key=True)
#     lati = Column(Float, nullable=False)
#     long = Column(Float, nullable=False)
#     roadmap_id = Column(String, ForeignKey('roadmap.id'), nullable=False)

# class Tag(Base):
#     __tablename__ = 'tag'
#     name = Column(String, nullable=False, primary_key=True)

# engine = create_engine('sqlite:///project.db')
# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)
# session = Session()
# user = User()
# user.id = 'bla'
# user.name = 'bla2'
# user.username = 'bla3'
# user.password_hash = 'bla4'
# user.password_salt = 'bla5'
# user.followers_counter = 1
# user.following_counter = 2

# session.add(user)
# session.commit()
# user = session.get(User, 'bla')
# print(user.username)
