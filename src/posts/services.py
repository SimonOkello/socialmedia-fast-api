from sqlalchemy.orm import Session

from src.posts.models import Post

from .schemas import CreatePost


def get_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def query_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id)


def create_post(db: Session, request: CreatePost):
    post = Post(
        title=request.title, content=request.content, published=request.published,)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
