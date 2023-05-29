from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from decouple import config
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.authentication.schemas import TokenData
from src.database import get_db
from src.users import models

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret_key = config('SECRET_KEY')


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def hash_password(password):
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    expires_delta = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms='H256')
        user_id: str = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, secret_key, algorithms='H256')
        user_id: str = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
