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

