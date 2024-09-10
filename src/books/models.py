from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT

from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(20), nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(TEXT(), nullable=False)

    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="SET NULL", ondelete="SET NULL"), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id', onupdate="SET NULL", ondelete="SET NULL"), nullable=False)
    review_text = Column(TEXT, nullable=False)
    rating = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship(
        "User", backref="users", foreign_keys=[user_id]
    )
    book = relationship(
        "Book", backref="books", foreign_keys=[book_id]
    )
