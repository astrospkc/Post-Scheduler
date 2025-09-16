from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

Database_url = os.getenv("DATABASE_URL")


engine = create_engine(Database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
