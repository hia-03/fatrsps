from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,model_validator,field_validator


class UsrSchemos(BaseModel):
    username:str
    email:EmailStr
    role:str
    password:str
    confpas:str


    @model_validator(mode="before")
    def paswordvalidate(value):
        if value['password'] != value['confpas']:
            raise ValueError('Wash Parol Ne sovpadaet')
        return value
    


