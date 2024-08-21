# schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    nom_user: str
    prenom: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id_user: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

from typing import Optional
from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nom_user: Optional[str] = None
    prenom: Optional[str] = None