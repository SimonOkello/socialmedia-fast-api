from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from urllib.parse import quote

# URL-encode the password
encoded_password = quote(config('DATABASE_PASSWORD'))

SQLALCHEMY_DATABASE_URL = f"postgresql://{config('DATABASE_USER')}:{encoded_password}@{config('DATABASE_HOST')}/{config('DATABASE_NAME')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
