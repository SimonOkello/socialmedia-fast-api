from fastapi import FastAPI
from src.authentication import authrouter

from src.posts import postsrouter
from src.users import usersrouter

from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authrouter.router)
app.include_router(usersrouter.router)
app.include_router(postsrouter.router)
