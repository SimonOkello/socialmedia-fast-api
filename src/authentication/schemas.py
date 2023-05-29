import email
from pydantic import BaseModel, EmailStr


class AuthUser(BaseModel):
    email: EmailStr
    access_token: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
