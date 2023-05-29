import email
from email import message
from pydantic import BaseModel, EmailStr


class AuthUser(BaseModel):
    status: bool
    message: str = 'Login successful'
    email: EmailStr
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    user_id: str | None = None
