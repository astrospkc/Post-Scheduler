from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
# import os
# from dotenv import load_dotenv
# load_dotenv()
DATABASE_URL='postgresql://neondb_owner:npg_WEqepI4Khy5x@ep-soft-leaf-ad4tz7fy-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Database_url = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
