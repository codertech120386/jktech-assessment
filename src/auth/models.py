from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('email', name='unique_constraint'),)
