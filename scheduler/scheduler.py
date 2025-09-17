from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy.orm import Session
from database import SessionLocal
from models.post import Post, PostStatus
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DATABASE_URL")

jobstores = {
    "default":SQLAlchemyJobStore(
        url=db_url,
        tablename="apscheduler_jobs"
    )
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

def job_listener(event):
    if event.exception:
        print(f"[{datetime.utcnow()}] Job {event.job_id} failed: {event.exception}")
    else:
        print(f"[{datetime.utcnow()}] Job {event.job_id} completed successfully!")
        

scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        

def publish_post_job(post_id):
    print("publishing job")
    db:Session = SessionLocal()
    print("post_id", post_id)
    post_id= int(post_id)
    post = db.query(Post).filter(Post.id==post_id).first()
    if post and post.status==PostStatus.scheduled:
        post.status =PostStatus.published
        db.commit()
        print(f"[{datetime.utcnow()}] Post {post.id} published!")
        db.refresh(post)
    db.close()

def print_message(msg):
    print("message: ", msg)

def scheduled_post_job(post_id:int, run_at:datetime):
    print("scheduling post job: ", run_at)
    trigger = DateTrigger(run_date=run_at)
    scheduler.add_job(publish_post_job,'date', run_date=str(run_at), args=(str(post_id),), id=str(post_id))


def get_all_jobs():
    jobs = scheduler.get_jobs()
    
    serialized_jobs = []

    for job in jobs:
        serialized_jobs.append({
            "id": job.id,
            "name": job.name,
            "func": job.func_ref,
            "args": job.args,
            "kwargs": job.kwargs,
            "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger),
        })

    return serialized_jobs

def delete_all_jobs():
    scheduler.remove_all_jobs()
    return {"message": "All jobs deleted"}


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
