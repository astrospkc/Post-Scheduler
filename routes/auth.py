from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import crud.user as crud
from models.user import User
from schemas.user import UserOut, UserCreate
from core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionLocal
import core

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter()



# register user 
@router.post("/register", response_model=core.TokenResponse) 
def register(user:UserCreate, db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user) 
    print("new_user: ", new_user)
    # jwt payload
    data = {  
            "sub": new_user.id,
            "name":new_user.name,
            "email":new_user.email}
    access_token = create_access_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"success":True,"access_token": access_token,
    "token_type": "bearer",  
    "user": {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        
    }}

# login user 
@router.post("/token")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=form_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email ")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.id,
            "name":user.name,
            "email":user.email
        }, expires_delta=access_token_expires
    )
    return {"Success":True,
        "access_token": access_token,
    "token_type": "bearer",  
    "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "full_name": user.full_name
    }}


# # Protected route 
# @router.get("/me", response_model=UserOut)
# def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    import jwt
    from core.security import SECRET_KEY, ALGORITHM
    from jwt.exceptions import InvalidTokenError

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = crud.get_user_by_name(db, name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user