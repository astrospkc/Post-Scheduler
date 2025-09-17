from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class PostStatus(str, Enum):
    scheduled = "scheduled"
    published = "published"

class PostBase(BaseModel):
    title:str
    description:str 
    scheduled_time:datetime

class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PostOut(PostBase):
    id:int
    user_id:int
    title:str
    description:str
    status:PostStatus

    class Config:
        from_attributes = True