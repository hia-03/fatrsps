from sqlalchemy import create_engine, Column, Integer, Sequence, String, Date, Float, BIGINT,ForeignKey

from sqlalchemy.orm import declarative_base,relationship,DeclarativeBase

import datetime
from datetime import datetime

from sqlalchemy import DateTime,DATETIME


class BaseModel(DeclarativeBase):
    pass



class UsersModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    password = Column(String)
    role = Column(String,default='user')

    Session = relationship("SessionModels",back_populates="user")
    notes = relationship("NoteModels", back_populates="user")




class SessionModels(BaseModel):
    __tablename__="sessionmod"
    id = Column(Integer,primary_key=True)
    token = Column(String)
    create_at = Column(DateTime,default=datetime.now())
    user_id = Column(Integer,ForeignKey("users.id"))

    user = relationship("UsersModel",back_populates="Session")



class NoteModels(BaseModel):
    __tablename__ = "notemods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UsersModel", back_populates="notes")


