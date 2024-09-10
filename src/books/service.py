import math

import pandas as pd
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.json import pydantic_encoder
from psycopg2._psycopg import Decimal
from sqlalchemy import func, desc
from icecream import ic
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from dotenv import load_dotenv

from database import SessionLocal
from src.utils import generic_response, upload_files_to_s3, convert_file_content_to_df

from .models import Book, Review

load_dotenv()
date_format = "%Y-%m-%d"


def create_book_in_db(title: str, author: str, genre: str, year_published: int, summary: str, session: SessionLocal):
    try:
        book = Book(
            title=title,
            author=author,
            genre=genre,
            year_published=year_published,
            summary=summary
        )

        session.add(book)
        session.commit()
        session.refresh(book)

        created = book.created.strftime(date_format)
        updated = book.updated.strftime(date_format)

        return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
                'year_published': book.year_published, 'summary': book.summary, 'created': created, 'updated': updated}
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def update_book_in_db(book_id: int, title: str, author: str, genre: str, year_published: int, summary: str,
                      session: SessionLocal):
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
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def delete_book_in_db(book_id: int, session: SessionLocal):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()

        if not book:
            return generic_response(
                {"error": True, "message": "Book does not exist", "status_code": status.HTTP_400_BAD_REQUEST})

        session.delete(book)
        session.commit()

        return {'message': 'Book deleted successfully', 'id': book_id}
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_book_by_id_from_db(book_id: int, session: SessionLocal):
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        ic(book)
        if not book:
            return False

    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")

    created = book.created.strftime(date_format)
    updated = book.updated.strftime(date_format)

    return {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre,
            'summary': book.summary, 'year_published': book.year_published, 'created': created,
            'updated': updated}


def fetch_all_books_from_db(active_page: int, session: SessionLocal):
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
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_reviews_by_book_id_from_db(active_page: int, book_id: int, session: SessionLocal):
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
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def check_existing_review(user_id: int, book_id: int, session: SessionLocal):
    try:
        review = session.query(Review).filter(Review.book_id == book_id).filter(Review.user_id == user_id).first()

        if review:
            return True
        return False
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


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
        ic(e)
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


def fetch_latest_rating_given_by_user(user_id: int, session: SessionLocal):
    try:
        review = session.query(Review).filter(Review.user_id == user_id).order_by(desc(Review.created)).first()
        if not review:
            return False
        rating = review.rating
        
        book = session.query(Book).filter(Book.id == review.book_id).first()
        genre = book.genre

        return {'rating': rating, 'genre': genre}

    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def get_books_data_for_training_model(book_ids: list[int], books: list[Book], books_data: list[list[any]],
                                      session: SessionLocal):
    try:
        for book in books:
            book_ids.append(book.id)

        review_ratings = session.query(Book.title, Book.genre, func.avg(Review.rating).label('average_rating')) \
            .join(Book, Review.book_id == Book.id) \
            .where(Review.book_id.in_(book_ids)) \
            .group_by(Review.book_id, Book.title, Book.genre) \
            .all()

        for review_rating in review_ratings:
            average_rating = jsonable_encoder(review_rating.average_rating, custom_encoder={Decimal: pydantic_encoder})
            if average_rating > 0:
                books_data.append([review_rating.title, review_rating.genre, round(average_rating, 2)])

        return books_data
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


def fetch_books_and_their_average_ratings(session: SessionLocal):
    try:
        offset = 0
        limit = 10
        end = offset + limit
        books_count = session.query(Book).count()
        book_ids = []
        books_data = [['title', 'genre', 'rating']]

        while end < books_count:
            books = session.query(Book).offset(offset).limit(limit).all()
            end += limit
            offset += limit
            books_data = get_books_data_for_training_model(book_ids=book_ids, books=books, books_data=books_data,
                                                        session=session)
            book_ids = []

        if end - books_count < limit:
            books = session.query(Book).offset(offset).limit(limit).all()
            books_data = get_books_data_for_training_model(book_ids=book_ids, books=books, books_data=books_data,
                                                        session=session)

        # create csv for use by the model for training
        df = pd.DataFrame(books_data[1:], columns=books_data[0])
        df.to_csv('books_data.csv')
        upload_files_to_s3(file_name='books_data.csv')
    except Exception as e:
        ic(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong .. please try again later.")


# Custom scoring function using mean distance between neighbors
def custom_scorer_knn(estimator, x):
    distances, indices = estimator.kneighbors(x)
    ic(distances, indices)
    return np.mean(distances)


async def train_model_for_recommendations(session: SessionLocal):
    fetch_books_and_their_average_ratings(session)
    df = convert_file_content_to_df(file_name='books_data.csv')

    label_genre = LabelEncoder()
    df['genre_encoded'] = label_genre.fit_transform(df['genre'])

    # Normalize ratings
    scaler = StandardScaler()
    df['rating_scaled'] = scaler.fit_transform(df[['rating']])

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    upload_files_to_s3('scaler.pkl')

    # Split the data into training and testing
    x = df[['genre_encoded', 'rating_scaled']]
    x_train, x_test = train_test_split(x, test_size=0.2, random_state=42)

    # Define the parameter grid to search over
    param_grid = {
        'n_neighbors': [3, 5, 7, 10],  # List of neighbor values to try
        'metric': ['euclidean', 'manhattan', 'chebyshev', 'cosine']
    }

    model_knn = NearestNeighbors()

    # Use GridSearchCV to search over hyperparameters
    grid_search = GridSearchCV(
        estimator=model_knn,
        param_grid=param_grid,
        scoring=custom_scorer_knn,  # Pass the custom scoring function directly
        cv=5,  # 5-fold cross-validation
        verbose=2
    )

    # Fit the grid search model
    grid_search.fit(x_train)

    # Model training
    x = df[['genre_encoded', 'rating_scaled']]
    model_knn = NearestNeighbors(n_neighbors=grid_search.best_params_["n_neighbors"],
                                 metric=grid_search.best_params_["metric"])
    model_knn.fit(x)

    # Save the model to a file
    with open('knn_model.pkl', 'wb') as f:
        pickle.dump(model_knn, f)

    upload_files_to_s3('knn_model.pkl')
