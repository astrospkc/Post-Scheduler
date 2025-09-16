from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base 


class Post(Base):
    __tablename__="posts"
    id=Column(Integer, primary_key=True, index=True) 
    user_id=Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title=Column(String, nullable=False)
    description=Column(String)