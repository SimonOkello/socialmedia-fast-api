from src.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    date_created = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    # owner = relationship("User", back_populates="posts")
