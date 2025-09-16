from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import Annotated
from database import SessionLocal
from models.post import Post 
from schemas.post import PostCreate, PostUpdate , PostOut
from core.security import get_current_active_user
from models.user import User
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/createPost", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post( post:PostCreate,current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    print("current user: ", current_user)
    current_user_id = current_user.id
    print("current user id: ", current_user_id)
    db_post = Post(**post.dict(), user_id=current_user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# @router.put("/updatePost/{post_id}")
# def update_post():

# @router.delete("/deleteAllPost")
# def delete_all_post():

# @router.delete("/deletePost/{post_id}")
# def delete_post():

# @router.get("/getAllPost")
# def get_all_post():

# @router.get("/getPost/{post_id}")
# def get_post():