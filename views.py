from fastapi import Depends, FastAPI,HTTPException,Request,Response
from sqlalchemy.orm import Session
from database import get_my_db
from models import *
from schem import *
from manage import app
from helpers import get_hashed_password
account = FastAPI()


@app.post("/register")
async def register_view(user_data:UsrSchemos,request:Request,response:Response,db:Session = Depends(get_my_db)):

    hash_pas = get_hashed_password(user_data.password)
    user = UsersModel(username=user_data.username,email=user_data.email,password=hash_pas,role=user_data.role)

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":"create user succesfully"}
    



