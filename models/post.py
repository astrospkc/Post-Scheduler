from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database import Base

class PostStatus(str, enum.Enum):
    scheduled = "scheduled"
    published = "published"

class Post(Base):
    __tablename__="posts"
    id=Column(Integer, primary_key=True, index=True) 
    user_id=Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title=Column(String, nullable=False)
    description=Column(String)
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(PostStatus, name="poststatus" ,  native_enum=False), default=PostStatus.scheduled)

    user = relationship("User", back_populates="posts")
    created_at=Column(DateTime, default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)