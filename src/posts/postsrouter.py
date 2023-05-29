from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from src.posts import services

from src.posts.schemas import CreatePost, Post
from .models import Base
from src.database import engine, get_db


Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/v1/posts",
                   tags=["Posts"],)


@router.get('/latest')
def latest_posts(db: Session = Depends(get_db)):
    posts = services.get_posts(db)
    latest_posts = posts[len(posts)-1]
    return latest_posts


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[Post])
def posts(db: Session = Depends(get_db)):
    posts = services.get_posts(db)
    return posts


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = services.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    post = services.create_post(db, post)
    return post


@router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = services.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = services.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)