
from fastapi import Depends, FastAPI,HTTPException,Request,Response
import uvicorn
app = FastAPI()
from sqlalchemy.orm import Session
from database import get_my_db
from models import *
from schem import *
from helpers import *
import uuid


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




@app.post("/create_note",dependencies=[Depends(is_authenticated)])
async def createnot(user_data:NoteSchemas,current_user:UsersModel = Depends(is_authenticated), db:Session = Depends(get_my_db)):
    note = NoteModels(name=user_data.name, desc=user_data.desc, user_id=current_user.id)

    db.add(note)
    db.commit()
    db.refresh(note)
    
@app.get("/notesмview", dependencies=[Depends(is_authenticated)])
async def select_all_notes(current_user: UsersModel = Depends(is_authenticated),db: Session = Depends(get_my_db)):
    notes = db.query(NoteModels).filter(NoteModels.user_id == current_user.id).all()
    return {"status": "success", "data": notes}


@app.get("/notes",dependencies=[Depends(is_authenticated)])
async def note_view_for_users(current_user:UsersModel = Depends(is_authenticated), db:Session = Depends(get_my_db)):
    notes = db.query(NoteModels).filter(NoteModels.user_id == current_user.id).all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="У вас нет заметка")
    return notes

@app.get("/user-list-admin",dependencies=[Depends(is_authenticated)])
async def admin_view_users(current_user:UsersModel = Depends(is_authenticated), db:Session = Depends(get_my_db)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступ только адмнистратор")
    notes = db.query(UsersModel).all()
    return notes


@app.put("/noteupdate/{note_id}",dependencies=[Depends(is_authenticated)])
async def note_update_by_admin(note_id:int,note_data:NoteSchemas,current_user:UsersModel = Depends(is_authenticated),db:Session = Depends(get_my_db)):
    note = db.query(NoteModels).filter(NoteModels.id == note_id, NoteModels.user_id == current_user.id).first()
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступ только адмнистратор")
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена.")
    note.name = note_data.name
    note.desc = note_data.desc
    db.commit()
    db.refresh(note)
    return note

@app.delete("/admin-notes-delete/{note_id}",dependencies=[Depends(is_authenticated)])
async def note_delete_by_admin(note_id:int,current_user:UsersModel = Depends(is_authenticated ),db:Session = Depends(get_my_db)):
    note = db.query(NoteModels).filter(NoteModels.id == note_id, NoteModels.user_id == current_user.id).first()
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступ только адмнистратор.")
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена.")
    db.delete(note)
    db.commit()
    return {"message": "Заметка успешно удалена."}



if __name__ == "__main__":
    print('table created succesfully')
    uvicorn.run("manage:app", host='127.0.0.1', port=8000, reload=True)