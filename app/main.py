from fastapi import Depends, FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from app import crud
from app.schemas import CreatePost
import time
from decouple import config
from sqlalchemy.orm import Session
from .models import Base
from .database import SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/api/v1/posts/latest')
def latest_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=0, limit=10)
    latest_posts = posts[len(posts)-1]
    return {
        'status': True,
        'message': 'Latest posts',
        'data': latest_posts
    }


@app.get('/api/v1/posts', status_code=status.HTTP_200_OK)
async def posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=0, limit=10)
    return {
        'status': True,
        'message': 'Posts',
        'data': posts
    }


@app.get('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK)
async def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return {
        'status': True,
        'message': 'Post detail',
        'data': post
    }


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    post = crud.create_post(db, post)
    return {
        'status': True,
        'message': 'Post created successfully',
        'data': post
    }


@app.delete('/api/v1/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    db.delete(post)
    db.commit()
    return {
        'status': True,
        'message': 'Post deleted successfully'
    }
