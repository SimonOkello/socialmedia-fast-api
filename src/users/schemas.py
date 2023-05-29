import email
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
