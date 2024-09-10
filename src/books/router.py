import asyncio

from fastapi import APIRouter, Depends, BackgroundTasks, status
from fastapi.security import HTTPBearer
from icecream import ic

from database import SessionLocal, get_db
from src.utils import verify_token, generic_response

from .schema import CreateOrUpdateBookSchema, CreateReviewSchema
from .controller import add_book, update_book, delete_book, fetch_books, fetch_book_by_id, fetch_reviews_by_book_id, \
    fetch_book_summary_and_aggregate_ratings_by_id, add_review_for_book_by_id, \
    get_all_books_with_average_ratings, train_model_for_reco

auth_scheme = HTTPBearer()

books_router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Book routes Not found"}},
)


@books_router.post('/')
def create_book(book: CreateOrUpdateBookSchema, session: SessionLocal = Depends(get_db), token=Depends(auth_scheme),
                user_data=Depends(verify_token)):
    return add_book(book=book, session=session)


@books_router.patch('/{book_id}')
def edit_book(book_id: int, book: CreateOrUpdateBookSchema, session: SessionLocal = Depends(get_db),
              token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return update_book(book_id=book_id, book=book, session=session)


@books_router.delete('/{book_id}')
def remove_book(book_id: int, session: SessionLocal = Depends(get_db), token=Depends(auth_scheme),
                user_data=Depends(verify_token)):
    return delete_book(book_id=book_id, session=session)


@books_router.get('/train-model')
async def train_model(session: SessionLocal = Depends(get_db),
                      token=Depends(auth_scheme), user_data=Depends(verify_token)):
    asyncio.create_task(train_model_for_reco(session=session))
    return generic_response({"data": "Task is processing in background", "status_code": status.HTTP_201_CREATED})


@books_router.get('/all-books-with-average-ratings')
def books_with_avg_ratings(session: SessionLocal = Depends(get_db),
                           token=Depends(auth_scheme), user_data=Depends(verify_token)):
    return get_all_books_with_average_ratings(session=session)


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
