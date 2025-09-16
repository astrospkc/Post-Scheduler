from datetime import datetime, timedelta, timezone
from typing import Annotated
from models.user import User
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session 
import os 
from dotenv import load_dotenv
load_dotenv()

from database import get_db

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserBase(BaseModel):
    id:int
    name:str
    email:EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int

class TokenResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str
    user: UserBase  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data:dict, expires_delta:timedelta|None=None):
    to_encode = data.copy()
    print("to encode: ", to_encode)
    expire = datetime.now(timezone.utc) +(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token):
    try:
        payload =jwt.decode(token, secret_key)
        print("payload: ", payload)
        return payload
    except:
        print("token not valid")
        raise Exception("wrong token")


async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db)):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        # p = verify_token(token)
        # print("verify token: ", p)
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        print("payload: ", payload)
        
        id: str = payload.get("sub")
        print("id: ", id)
        if id is None:
            raise Exception("Could not validate credentials")
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise Exception("invalid token")
    user = db.query(User).filter(User.id == int(token_data.id)).first() 
    print("user: ", user.id)
    if user is None:
        raise Exception("no user")
    return user

async def get_current_active_user(current_user:Annotated[User, Depends(get_current_user)]):
    print("current user: ", current_user.id)
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user