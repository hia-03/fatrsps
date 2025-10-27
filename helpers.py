from passlib.hash import pbkdf2_sha256
from models import *
from database import get_my_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,Request,Response,status
from database import SessionLocal

def get_hashed_password(password:str):
    res = pbkdf2_sha256.hash(password)
    print(res)
    return res



def verify_password(password:str,password_hash:str):
    return pbkdf2_sha256.verify(password,password_hash)

def authenticate(username:str,password:str):
    db = SessionLocal()
    user = db.query(UsersModel).filter(UsersModel.username==username).first()
    if user:
        is_correct_password = verify_password(password, user.password)
        if is_correct_password:
            db.close()
            return user
        db.close()
    return None

    


def is_authenticated(request:Request):
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
    session_db = get_my_db()
    db = next(session_db)
    session = request.cookies.get("session_key")
    if session:
        token = db.query(SessionModels).filter(SessionModels.token == session).first()
        if token:
            return token.user
        raise credentials_error
    return credentials_error
