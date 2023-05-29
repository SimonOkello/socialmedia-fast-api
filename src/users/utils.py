from passlib.context import CryptContext


def hash_password(password):
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(password)
    return hashed_password
