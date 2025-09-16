from pydantic import BaseModel

class PostBase(BaseModel):
    title:str
    description:str 


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id:int
    user_id:int
    title:str
    description:str

    class Config:
        from_attributes = True