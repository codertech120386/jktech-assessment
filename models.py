from database import engine
from src.auth import User
from src.books import Book, Review


def create_db_tables_from_models():
    User.metadata.create_all(bind=engine)
    Book.metadata.create_all(bind=engine)
    Review.metadata.create_all(bind=engine)
