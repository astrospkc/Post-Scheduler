from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base 


class PostAnalytics(Base):
    __tablename__="post_analytics"
    id=Column(Integer, primary_key=True, index=True)
    post_id=Column(Integer, ForeignKey("posts.id"), index=True, nullable=False)
    total_reactions=Column(Integer, nullable=False, default=0)
    total_comments=Column(Integer, nullable=False, default=0) 
    total_shares=Column(Integer, nullable=False, default=0) 
    total_impressions=Column(Integer, nullable=False, default=0)
    last_calculated_at=Column(DateTime(timezone=True), default=func.now())
    