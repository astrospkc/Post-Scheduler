from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import Annotated
from database import SessionLocal
from models.post import Post 
from schemas.post import PostCreate, PostUpdate , PostOut
from core.security import get_current_active_user
from models.user import User
from datetime import datetime
from datetime import timezone
import pytz
from scheduler import scheduled_post_job, get_all_jobs, delete_all_jobs
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
    ist = pytz.timezone('Asia/Kolkata')
    if post.scheduled_time.tzinfo is None:
    # naive datetime, localize it
        post_scheduled_time_ist = ist.localize(post.scheduled_time)
    else:
    # aware datetime, convert timezone
        post_scheduled_time_ist = post.scheduled_time.astimezone(ist)

    print("scheduled time and now time: ",post.scheduled_time, post_scheduled_time_ist, datetime.now(ist))
    if(post_scheduled_time_ist > datetime.now(ist)):
        db_post = Post(**post.dict(), user_id=current_user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        scheduled_post_job(db_post.id, post_scheduled_time_ist)
        return db_post
    else:
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

@router.get("/getAllJobs")
def getAllJobs():
    jobs = get_all_jobs()
    # print("jobs: ", jobs)
    return jobs
@router.delete("/deleteAllJobs")
def deleteAllJobs(db:Session=Depends(get_db)):
    msg =delete_all_jobs()
    return msg

@router.put("/updatePost/{post_id}", response_model=PostUpdate, status_code=status.HTTP_201_CREATED)
def update_post(post:PostUpdate, post_id:int, current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    print("db_post: ", db_post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to update this post")
    db_post.title = post.title if post.title else db_post.title
    db_post.description = post.description if post.description else db_post.description
    db.commit()
    db.refresh(db_post)
    return db_post

    
@router.delete("/deleteAllPost")
def delete_all_post(current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    db.query(Post).filter(Post.user_id==current_user.id).delete()
    db.commit()
    return {"message": "All posts deleted"}

@router.delete("/deletePost/{post_id}")
def delete_post(post_id:int, current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted"}

@router.get("/getAllPost")
def get_all_post(current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.user_id==current_user.id).all()
    return db_post

@router.get("/getPost/{post_id}")
def get_post(post_id:int, current_user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post