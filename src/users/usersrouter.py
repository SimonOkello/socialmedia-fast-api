from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.database import get_db

from src.users import schemas, services


router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = services.get_users(db)

    return users


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = services.create_user(db, user)

    return user
