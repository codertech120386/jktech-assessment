import math

from fastapi import HTTPException, status
from sqlalchemy import func
from icecream import ic

from database import SessionLocal
from src.utils import generic_response

from .models import Book, Review

date_format = "%Y-%m-%d"


def create_book_in_db(title: str, author: str, genre: str, year_published: int, session: SessionLocal):
    try:
        book = Book(
            title=title,
            author=author,
            genre=genre,
            year_published=year_published
        )

        session.add(book)
        session.commit()
        session.refresh(book)

        created = book.created.strftime(date_format)
        updated = book.updated.strftime(date_format)

        return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
                'year_published': book.year_published, 'created': created, 'updated': updated}
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def update_book_in_db(book_id, title, author, genre, summary, year_published, session):
    try:
        book_query = session.query(Book).filter(Book.id == book_id)
        book = book_query.first()

        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        book_query.update({
            'title': title,
            'author': author,
            'genre': genre,
            'summary': summary,
            'year_published': year_published,
        })

        session.commit()
        session.refresh(book)

        created = book.created.strftime(date_format)
        updated = book.updated.strftime(date_format)

        return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
                'summary': book.summary, 'year_published': book.year_published, 'created': created, 'updated': updated}
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def delete_book_in_db(book_id, session):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()

        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        session.delete(book)
        session.commit()

        return {'message': 'Book deleted successfully', 'id': book_id}
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_book_by_id_from_db(book_id, session):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")
    if not book:
        return False

    created = book.created.strftime(date_format)
    updated = book.updated.strftime(date_format)

    return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
            'summary': book.summary, 'year_published': book.year_published, 'created': created,
            'updated': updated}


def fetch_all_books_from_db(active_page, session):
    try:
        books_query = session.query(Book)
        limit = 10
        offset = (active_page - 1) * limit
        books = books_query.offset(offset).limit(limit).all()
        total_books = books_query.count()

        total_pages = math.ceil(total_books / limit)
        response = {'totalPages': total_pages, 'activePage': active_page, 'books': []}
        for book in books:
            created = book.created.strftime(date_format)
            updated = book.updated.strftime(date_format)

            row = {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
                   'summary': book.summary, 'year_published': book.year_published, 'created': created,
                   'updated': updated}
            response['books'].append(row)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_reviews_by_book_id_from_db(active_page, book_id, session):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return False

        reviews_query = session.query(Review).filter(Review.book_id == book.id)

        limit = 10
        offset = (active_page - 1) * limit
        reviews = reviews_query.join(Review.user).offset(offset).limit(limit).all()

        total_reviews = reviews_query.count()
        total_pages = math.ceil(total_reviews / limit)
        response = {'totalPages': total_pages, 'activePage': active_page, "book_id": book_id, 'reviews': []}
        for review in reviews:
            created = book.created.strftime(date_format)
            updated = book.updated.strftime(date_format)

            row = {'id': review.id, 'user_id': review.user_id, 'name': review.user.name,
                   'review_text': review.review_text,
                   'rating': review.rating, 'created': created,
                   'updated': updated}
            response['reviews'].append(row)

        return response

    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def check_existing_review(user_id: int, book_id: int, session: SessionLocal):
    review = session.query(Review).filter(Review.book_id == book_id).filter(Review.user_id == user_id).first()

    if review:
        return True
    return False


def create_review_in_db(user_id: int, book_id: int, review_text: str, rating: int, session: SessionLocal):
    try:
        review = Review(
            user_id=user_id,
            book_id=book_id,
            review_text=review_text,
            rating=rating
        )

        session.add(review)
        session.commit()
        session.refresh(review)

        created = review.created.strftime(date_format)
        updated = review.updated.strftime(date_format)

        return {'id': review.id, 'book_id': review.book_id, 'user_id': review.user_id,
                'review_text': review.review_text,
                'rating': review.rating, 'created': created, 'updated': updated}
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_summary_and_avg_ratings_of_book_by_id_from_db(book_id: int, session: SessionLocal):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return False

        average_rating = session.query(Review).with_entities(func.avg(Review.rating).label('average_rating')).join(
            Review.book).filter(Review.book_id == book.id).scalar()

        return {'book_id': book.id, 'summary': book.summary, 'average_rating': average_rating}

    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")
