from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, Response
from sqlalchemy.orm import Session

from src.posts import postsrouter
from src.users import usersrouter

from .models import Base
from .database import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(postsrouter.router)
app.include_router(usersrouter.router)
