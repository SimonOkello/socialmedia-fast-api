from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    date_created: datetime

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass
