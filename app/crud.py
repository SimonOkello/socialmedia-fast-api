from sqlalchemy.orm import Session

from . models import Post
from .schemas import CreatePost


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post: CreatePost):
    post = Post(
        title=post.title, content=post.content, published=post.published)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
