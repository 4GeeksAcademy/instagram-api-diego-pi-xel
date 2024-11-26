import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla intermedia para la relación de seguidores
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table user
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)  # Username for the user.
    email = Column(String(120), unique=True, nullable=False)  # Email for the user.
    password = Column(String(128), nullable=False)  # Password for the user.
    profile_picture = Column(String(255), nullable=True)  # Profile picture for the user.
    bio = Column(String(160), nullable=True)  # Bio for the user.
    created_at = Column(DateTime, default=func.current_timestamp())  # Timestamp for user creation.

    # Relaciones
    posts = relationship('Post', backref='author', lazy=True)  # Relationship with pots.
    comments = relationship('Comment', backref='user', lazy=True)  # Relationship with comments.
    likes = relationship('Like', backref='user', lazy=True)  # Relationship with likes.
    following = relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref='followers'
    )

class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table post
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # User who created the post.
    image_url = Column(String(255), nullable=False)  # Url for the post's image.
    caption = Column(Text, nullable=True)  # Caption for the post
    created_at = Column(DateTime, default=func.current_timestamp())  # Timestamp for post creation.

    # Relaciones
    comments = relationship('Comment', backref='post', lazy=True)  # Relationship with comments.
    likes = relationship('Like', backref='post', lazy=True)  # Relationship with likes.

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table comment
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Post related to the comment.
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # User who made the comment.
    content = Column(Text, nullable=False)  # Content of the comment
    created_at = Column(DateTime, default=func.current_timestamp())  # Timestamp for comment creation.

class Like(Base):
    __tablename__ = 'like'
    # Here we define columns for the table like
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Post liked.
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # User who liked the post.
    created_at = Column(DateTime, default=func.current_timestamp())  # Timestamp for the like.

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
