from passlib.hash import pbkdf2_sha256
from models import *
from database import get_my_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_hashed_password(password:str):
    res = pbkdf2_sha256.hash(password)
    print(res)
    return res



def verify_hashpas(password,hashed,db:Session = Depends(get_my_db)):
    user = db.query(UsersModel).filter(UsersModel.password == hashed).first()
    return user.ve

    