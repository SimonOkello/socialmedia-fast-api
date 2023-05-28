from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, Response
from sqlalchemy.orm import Session
from src import posts

from .models import Base
from .database import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)
