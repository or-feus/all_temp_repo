from typing import Union, List, Optional

from sqlalchemy import Column, Integer, DateTime, String, VARCHAR, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.connect import Base


class Author(Base):
    __tablename__ = "author"

    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    name: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    avatar: Union[str, Column] = Column(Text, nullable=False)
    description: Union[str, Column] = Column(Text, nullable=False)

    posts = relationship("Post", back_populates="author")
    # posts_id: Union[int, Column] = Column(ForeignKey('author.id', ondelete='RESTRICT'), nullable=True)


class Post(Base):
    __tablename__ = "post"

    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    title: Union[str, Column] = Column(String(100), nullable=False)
    current_time: Union[DateTime, Column] = Column(DateTime, nullable=False)
    content: Union[str, Column] = Column(String(100000), nullable=False)
    status: Union[str, Column] = Column(VARCHAR(20), nullable=False)
    like_count: Union[int, Column] = Column(Integer, nullable=False, default=0)
    comment_count: Union[int, Column] = Column(Integer, default=0)

    author_id: Union[int, Column] = Column(ForeignKey('author.id'), nullable=True)
    author = relationship('Author', back_populates="posts")

