from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from database import SessionLocal, get_db
from src.utils import verify_token

from .schema import CreateBookSchema, UpdateBookSchema, CreateReviewSchema
from .controller import add_book, update_book, delete_book, fetch_books, fetch_book_by_id, fetch_reviews_by_book_id, \
    fetch_book_summary_and_aggregate_ratings_by_id, add_review_for_book_by_id

auth_scheme = HTTPBearer()

books_router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Book routes Not found"}},
)


@books_router.post('/')
def create_book(book: CreateBookSchema, session: SessionLocal = Depends(get_db), token=Depends(auth_scheme),
                user_data=Depends(verify_token)):
    return add_book(book, session)


@books_router.patch('/{book_id}')
def edit_book(book_id: int, book: UpdateBookSchema, session: SessionLocal = Depends(get_db),
              token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return update_book(book_id=book_id, book=book, session=session)


@books_router.delete('/{book_id}')
def remove_book(book_id: int, session: SessionLocal = Depends(get_db), token=Depends(auth_scheme),
                user_data=Depends(verify_token)):
    return delete_book(book_id=book_id, session=session)


@books_router.get('/')
def fetch_all_books(page: int = 1, session: SessionLocal = Depends(get_db),
                    token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return fetch_books(active_page=page, session=session)


@books_router.get('/{book_id}')
def fetch_book(book_id: int, session: SessionLocal = Depends(get_db),
               token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return fetch_book_by_id(book_id=book_id, session=session)


@books_router.get('/{book_id}/summary')
def fetch_book_summary_and_aggregate_ratings(book_id: int, session: SessionLocal = Depends(get_db),
                                             token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return fetch_book_summary_and_aggregate_ratings_by_id(book_id=book_id, session=session)


@books_router.get('/{book_id}/reviews')
def fetch_book_reviews(book_id: int, page: int = 1, session: SessionLocal = Depends(get_db),
                       token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return fetch_reviews_by_book_id(active_page=page, book_id=book_id, session=session)


@books_router.post('/{book_id}/reviews')
def add_book_review(book_id: int, review_schema: CreateReviewSchema, session: SessionLocal = Depends(get_db),
                    token=Depends(auth_scheme), user_data=Depends(verify_token)):
    user_id = user_data['id']

    return add_review_for_book_by_id(book_id=book_id, user_id=user_id, review_schema=review_schema, session=session)
