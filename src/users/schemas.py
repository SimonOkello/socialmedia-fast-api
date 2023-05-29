from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    date_created: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
