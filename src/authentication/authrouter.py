from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.authentication.utils import create_access_token, verify_password
from src.database import get_db

from src.authentication import schemas, services
from src.users.models import User


router = APIRouter(prefix='/api/v1/auth', tags=['Authentication'])


@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.AuthUser)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    verify_user_password = verify_password(
        user_credentials.password, user.password)
    if not verify_user_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    access_token = create_access_token(
        data={'user_id': user.id, 'email': user.email})
    return {'status':True,'email': user.email, 'access_token': access_token, 'token_type': 'Bearer'}
