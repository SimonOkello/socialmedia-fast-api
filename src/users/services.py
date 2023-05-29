from sqlalchemy.orm import Session

from src.users.utils import hash_password

from . models import User
from .schemas import UserCreate


def get_users(db: Session):
    return db.query(User).all()


# def get_post(db: Session, post_id: int):
#     return db.query(Post).filter(Post.id == post_id).first()

# def query_post(db: Session, post_id: int):
#     return db.query(Post).filter(Post.id == post_id)


def create_user(db: Session, request_data: UserCreate):
    hashed_password = hash_password(request_data.password)
    user = User(
        email=request_data.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
