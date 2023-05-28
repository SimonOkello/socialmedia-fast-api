from sqlalchemy.orm import Session

from . models import Post
from .schemas import CreatePost


def get_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def query_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id)


def create_post(db: Session, post: CreatePost):
    post = Post(
        title=post.title, content=post.content, published=post.published)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
