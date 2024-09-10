from pydantic import BaseModel


class CreateOrUpdateBookSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My first book",
                "author": "Dhaval Chheda",
                "genre": "AI Tech",
                "year_published": 2024,
                "summary": "This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary",
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
