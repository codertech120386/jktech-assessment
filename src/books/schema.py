from pydantic import BaseModel
from typing import Optional


class CreateBookSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My first book",
                "author": "Dhaval Chheda",
                "genre": "AI Tech",
                "year_published": 2024,
            }
        }


class UpdateBookSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My first book",
                "author": "Dhaval Chheda",
                "genre": "AI Tech",
                "year_published": 2024,
                "summary": "This is the summary of the book"
            }
        }


class CreateReviewSchema(BaseModel):
    review_text: str
    rating: int

    class Config:
        json_schema_extra = {
            "example": {
                "review_text": "This is an awesome book .. must read by everyone",
                "rating": 5,
            }
        }
