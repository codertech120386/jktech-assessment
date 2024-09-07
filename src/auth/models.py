from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    email = Column(String(50))
    # I don't think creating enum fields is a good idea
    # as when we add or remove something it leads to alter table and table locks
    # and I manage by validation in the backend itself
    password = Column(String(60))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('email', name='unique_constraint'),)
