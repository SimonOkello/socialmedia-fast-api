from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.authentication.utils import verify_password
from src.database import get_db

from src.authentication import schemas, services
from src.users.models import User


router = APIRouter(prefix='/api/v1/auth', tags=['Authentication'])


@router.post('/login', status_code=status.HTTP_200_OK)
def user_login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    verify_user_password = verify_password(
        user_credentials.password, user.password)
    if not verify_user_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    access_token = {}
    return access_token
