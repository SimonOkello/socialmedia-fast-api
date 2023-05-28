from fastapi import Depends, FastAPI, status, HTTPException
from h11 import Response
from app import crud
from app.schemas import CreatePost
from sqlalchemy.orm import Session
from .models import Base, Post
from .database import engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/api/v1/posts/latest')
def latest_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    latest_posts = posts[len(posts)-1]
    return {
        'status': True,
        'message': 'Latest posts',
        'data': latest_posts
    }


@app.get('/api/v1/posts', status_code=status.HTTP_200_OK)
def posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return {
        'status': True,
        'message': 'Posts',
        'data': posts
    }


@app.get('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK)
def post_detail(post_id: int, db: Session = Depends(get_db)):
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


@app.put('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = crud.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}


@app.delete('/api/v1/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = crud.query_post(db, post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return {'message':'Post deleted'}
