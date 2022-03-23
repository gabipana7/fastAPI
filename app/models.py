from sqlite3 import Timestamp
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# SQL Alchemy model, defines what the tables look like in DB
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # The foreign key that establishes the relation bethween user and posts (1:N rel)
    # ondelete is set to CASCADE, meaning deleting a user, delets all hist posts
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Create a owner property for the Post model that returns the relationship with the User class
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    