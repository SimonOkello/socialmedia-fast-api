from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config
from jose import JWTError, jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    secret_key = config('SECRET_KEY')
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt
