from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    """ SQLAlchemy model for the 'user' table."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Post(Base):
    """SQLAlchemy model for the 'posts' table."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(280))
    user_id = Column(Integer)
    # post_id = Column(Integer, ForeignKey('user.id'))

