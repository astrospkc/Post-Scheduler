from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title:str
    description:str 


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

    class Config:
        from_attributes = True