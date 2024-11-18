from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Post(Base):
    __tablename__ = "posts1"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    title = Column(String, nullable=False)             # Title of the post
    content = Column(Text, nullable=False)             # Content of the post
    published = Column(Boolean, default=True)          # Publication status
    created_at = Column(DateTime, default=func.now())  # Auto timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Updated timestamp



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, nullable=True)              # Name of the user
    email = Column(String, nullable=False, unique=True) # Email of the user (must be unique)
    password = Column(String, nullable=False)          # Hashed password
    is_active = Column(Boolean, default=True)          # Active status
    created_at = Column(DateTime, default=func.now())  # Auto timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto timestamp for updates
