from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name:str
    email:EmailStr
    password:str


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass 

class UserOut(UserBase):
    id:int 
    name:str
    email:EmailStr

    class Config:
        from_attributes = True  # tell pydantic that schema can read data directly from sqlalchemy model objects 
