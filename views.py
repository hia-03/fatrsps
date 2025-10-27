from fastapi import Depends, FastAPI,HTTPException,Request,Response
from sqlalchemy.orm import Session
from database import get_my_db
from models import *
from schem import *
from manage import app
import uuid
from helpers import get_hashed_password,verify_password,authenticate,is_authenticated
account = FastAPI()


@app.post("/register")
async def register_view(user_data:UsrSchemos,request:Request,response:Response,db:Session = Depends(get_my_db)):

    hash_pas = get_hashed_password(user_data.password)
    user = UsersModel(username=user_data.username,email=user_data.email,password=hash_pas,role=user_data.role)

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":"create user succesfully"}
    



@app.post("/login")
async def login_view(user_data:Loginschemas,response:Response,db:Session = Depends(get_my_db)):
    user = authenticate(user_data.username,user_data.password)
    if not user:
        raise ValueError('Inxel odam nest')

    session_id = db.query(SessionModels).filter(SessionModels.user_id == user.id).first()

    if not session_id:
        token = str(uuid.uuid4())
        session = SessionModels(token=token,user_id=user.id)
        db.add(session)
        db.commit()

        response.set_cookie(key="session_key",value=token,httponly=True)

        return f'Loged succesfully'


@app.post("/logout",dependencies=[Depends(is_authenticated)])
async def logout_view(response:Response,request:Request,db:Session = Depends(get_my_db)):
    session_key = request.cookies.get("session_key")
    session = db.query(SessionModels).filter(SessionModels.token == session_key).first()
    
    if session:
        db.delete(session)
        db.commit()
        response.delete_cookie("session_key")
        return {"message": "User logged out"}
    return {"message":"Not logged in user"}
