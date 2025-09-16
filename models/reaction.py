import enum
from sqlalchemy import Column, Integer, String , ForeignKey, Enum, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base 


class ReactionType(str, enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    EMPATHY="empathy"
    INTEREST="interest"
    APPRECIATION="appreciation"


class Reaction(Base):
    __tablename__="reactions"
    id = Column(Integer, primary_key=True, index=True)
    post_id=Column(Integer,ForeignKey("posts.id"), index=True, nullable=False)
    user_id=Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    reaction_type=Enum(ReactionType) 
    created_at=Column(DateTime(timezone=True), default=func.now())
    updated_at=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # user=relationship("User", back_populates="reactions")


