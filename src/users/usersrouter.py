from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.authentication.utils import get_current_user
from src.database import get_db

from src.users import schemas, services


router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    users = services.get_users(db)

    return users


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request_data: schemas.UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user = services.create_user(db, request_data)

    return user
