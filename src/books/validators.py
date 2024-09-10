def book_create_or_update_validations(title, author, year_published, genre, summary):
    errors = []
    if title is None or len(title) == 0:
        errors.append("Title is required for creating a book\n")
    if author is None or len(author) == 0:
        errors.append("Author is required for creating a book\n")
    if year_published is None:
        errors.append("Published Year is required for creating a book\n")
    if genre is None or len(genre) == 0:
        errors.append("Genre is required for creating a book\n")
    if summary is None or len(summary) == 0:
        errors.append("Summary is required for creating a book\n")
    if genre not in ['Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Horror']:
        errors.append("Genre must be Fantasy or Science Fiction or Romance or Mystery or Horror\n")

    return errors


def add_review_validations(rating):
    errors = []
    if rating < 0 or rating > 5:
        errors.append("Rating must be between 0 and 5\n")

    return errors
