import time
import asyncio

from fastapi import status
from fastapi.encoders import jsonable_encoder
from psycopg2._psycopg import Decimal
from pydantic.json import pydantic_encoder
from icecream import ic
import pandas as pd
import pickle

from src.utils import generic_response, errors_response
from database import SessionLocal

from .schema import CreateOrUpdateBookSchema, CreateReviewSchema
from .service import create_book_in_db, fetch_book_by_id_from_db, delete_book_in_db, update_book_in_db, \
    fetch_all_books_from_db, fetch_reviews_by_book_id_from_db, create_review_in_db, check_existing_review, \
    fetch_summary_and_avg_ratings_of_book_by_id_from_db, fetch_books_and_their_average_ratings, \
    train_model_for_recommendations
from .validators import book_create_or_update_validations, add_review_validations


def add_book(book: CreateOrUpdateBookSchema, session: SessionLocal):
    try:
        title, author, year_published, genre, summary = book.title, book.author, book.year_published, book.genre, book.summary
        errors = book_create_or_update_validations(title=title, author=author, year_published=year_published,
                                                   genre=genre, summary=summary)

        if len(errors) > 0:
            return errors_response(errors)

        book = create_book_in_db(title=title, author=author, genre=genre, year_published=year_published,
                                 summary=summary, session=session)

        return generic_response({"data": book, "status_code": status.HTTP_201_CREATED})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def update_book(book_id: int, book: CreateOrUpdateBookSchema, session: SessionLocal):
    try:
        title, author, year_published, genre, summary = book.title, book.author, book.year_published, book.genre, book.summary
        errors = book_create_or_update_validations(title=title, author=author, year_published=year_published,
                                                   genre=genre, summary=summary)

        if len(errors) > 0:
            return errors_response(errors)

        fetched_book = fetch_book_by_id_from_db(book_id=book_id, session=session)
        if not fetched_book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        updated_book = update_book_in_db(book_id=book_id, title=title, author=author, genre=genre, summary=summary,
                                         year_published=year_published, session=session)

        return generic_response({"data": updated_book, "status_code": status.HTTP_201_CREATED})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def delete_book(book_id: int, session: SessionLocal):
    try:
        fetched_book = fetch_book_by_id_from_db(book_id=book_id, session=session)
        if not fetched_book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})
        deleted_book_success_message = delete_book_in_db(book_id=book_id, session=session)

        return generic_response({"data": deleted_book_success_message, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def fetch_books(active_page: int, session: SessionLocal):
    try:
        all_books = fetch_all_books_from_db(active_page=active_page, session=session)

        return generic_response({"data": all_books, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def fetch_book_by_id(book_id: int, session: SessionLocal):
    try:
        book = fetch_book_by_id_from_db(book_id=book_id, session=session)
        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST}
            )
        return generic_response({"data": book, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def fetch_reviews_by_book_id(active_page: int, book_id: int, session: SessionLocal):
    try:
        book = fetch_reviews_by_book_id_from_db(active_page=active_page, book_id=book_id, session=session)
        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST}
            )
        return generic_response({"data": book, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def fetch_book_summary_and_aggregate_ratings_by_id(book_id: int, session: SessionLocal):
    try:
        book = fetch_book_by_id_from_db(book_id=book_id, session=session)
        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        book_summary_with_average_ratings = fetch_summary_and_avg_ratings_of_book_by_id_from_db(book_id=book_id,
                                                                                                session=session)

        json_result = jsonable_encoder(book_summary_with_average_ratings, custom_encoder={Decimal: pydantic_encoder})
        if json_result["average_rating"]:
            json_result["average_rating"] = round(json_result["average_rating"], 2)

        return generic_response({"data": json_result, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def add_review_for_book_by_id(book_id: int, user_id: int, review_schema: CreateReviewSchema, session: SessionLocal):
    try:
        book = fetch_book_by_id_from_db(book_id=book_id, session=session)
        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        existing_review = check_existing_review(book_id=book_id, user_id=user_id, session=session)
        if existing_review:
            return generic_response(
                {"error": True, "message": "You have already reviewed this book",
                 "status_code": status.HTTP_400_BAD_REQUEST})

        errors = add_review_validations(rating=review_schema.rating)
        if len(errors) > 0:
            return errors_response(errors)

        review = create_review_in_db(book_id=book_id, user_id=user_id, review_text=review_schema.review_text,
                                     rating=review_schema.rating, session=session)
        return generic_response({"data": review, "status_code": status.HTTP_201_CREATED})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


def get_all_books_with_average_ratings(session: SessionLocal):
    try:
        books_with_average_ratings = fetch_books_and_their_average_ratings(session=session)

        return generic_response({"data": books_with_average_ratings, "status_code": status.HTTP_200_OK})
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


async def train_model_for_reco(session: SessionLocal):
    try:
        await asyncio.create_task(train_model_for_recommendations(session=session))
    except Exception as e:
        print(e)
        return generic_response(
            {"message": "Something went wrong .. please try again later",
             "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})
