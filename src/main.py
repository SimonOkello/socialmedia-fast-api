from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, Response
from sqlalchemy.orm import Session
from src.posts import services

from src.posts.schemas import CreatePost, Post
from .models import Base
from .database import engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/api/v1/posts/latest')
def latest_posts(db: Session = Depends(get_db)):
    posts = services.get_posts(db)
    latest_posts = posts[len(posts)-1]
    return latest_posts


@app.get('/api/v1/posts', status_code=status.HTTP_200_OK, response_model=List[Post])
def posts(db: Session = Depends(get_db)):
    posts = services.get_posts(db)
    return posts


@app.get('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = services.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    post = services.create_post(db, post)
    return post


@app.put('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = services.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.delete('/api/v1/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = services.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
