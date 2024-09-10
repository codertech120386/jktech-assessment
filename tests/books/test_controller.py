import json
from src.books import Book, Review

from tests.test_setup import client, session
from tests.constants import full_register_payload, full_login_payload

full_book_create_payload = {
    "author": "Dhaval Chheda",
    "genre": "Science Fiction",
    "title": "My first book",
    "year_published": 2024,
    "summary": "This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary.This is a sample summary. This is a sample summary. This is a sample summary"
}

full_review_create_payload = {
    "rating": 5,
    "review_text": "This is an awesome book .. must read by everyone"
}


def get_token(client, register_payload=full_register_payload, login_payload=full_login_payload):
    client.post("/api/v1/auth/register", json=register_payload)
    response = client.post("/api/v1/auth/login", json=login_payload)

    return response.json()["data"]["token"]


def test_apis_fail_on_authorized_user_trying_to_access(client, session):
    token = "I am not authorized"
    bearer_token = f"Bearer {token}"

    api_response = client.post("/api/v1/books", json=full_book_create_payload,
                               headers={"Authorization": bearer_token})
    assert api_response.status_code == 401


def test_validation_failing_if_title_missing_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["title"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_genre_missing_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["genre"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_genre_is_not_from_the_list_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    full_book_create_payload_copy["genre"] = "Sports"

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_validation_failing_if_year_published_missing_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["year_published"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_author_missing_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["author"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_summary_missing_book_create(client, session):
    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["summary"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_book_creation_if_proper_payload_provided(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    api_response = client.post("/api/v1/books", json=full_book_create_payload,
                               headers={"Authorization": bearer_token})

    assert api_response.status_code == 201
    assert api_response.json()["data"]["id"] == 1
    assert session.query(Book).count() == 1


def test_validation_failing_if_title_missing_book_update(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["title"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.patch(f"/api/v1/books/{book_id}", json=full_book_create_payload_copy,
                            headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_genre_missing_book_update(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["genre"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.patch(f"/api/v1/books/{book_id}", json=full_book_create_payload_copy,
                            headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_year_published_missing_book_update(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["year_published"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.patch(f"/api/v1/books/{book_id}", json=full_book_create_payload_copy,
                            headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_author_missing_book_update(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    del full_book_create_payload_copy["author"]

    bearer_token = f"Bearer {get_token(client=client)}"
    response = client.patch(f"/api/v1/books/{book_id}", json=full_book_create_payload_copy,
                            headers={"Authorization": bearer_token})
    assert response.status_code == 422


def test_validation_failing_if_invalid_book_id_in_book_update(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    provided_book_id = 2
    response = client.patch(f"/api/v1/books/{provided_book_id}", json=full_book_create_payload,
                            headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_book_update_if_proper_payload_provided(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    full_book_create_payload_copy["author"] = "Dhaval Chheda Chheda"
    full_book_create_payload_copy["title"] = "Edited first Book"

    api_response = client.patch(f"/api/v1/books/{book_id}", json=full_book_create_payload_copy,
                                headers={"Authorization": bearer_token})

    assert api_response.status_code == 201
    assert api_response.json()["data"]["author"] == "Dhaval Chheda Chheda"
    assert api_response.json()["data"]["title"] == "Edited first Book"
    assert api_response.json()["data"]["year_published"] == 2024


def test_validation_failing_if_invalid_book_id_in_book_delete(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    provided_book_id = 2
    response = client.delete(f"/api/v1/books/{provided_book_id}", headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_book_delete_if_proper_payload_provided(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    assert session.query(Book).count() == 1

    book_id = create_book_response.json()["data"]["id"]

    api_response = client.delete(f"/api/v1/books/{book_id}", headers={"Authorization": bearer_token})

    assert api_response.status_code == 200
    assert session.query(Book).count() == 0


def test_getting_all_books_api(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"

    # first book created
    client.post("/api/v1/books", json=full_book_create_payload, headers={"Authorization": bearer_token})

    full_book_create_payload_copy = full_book_create_payload.copy()
    full_book_create_payload_copy["title"] = "Second Book"

    # second book created
    client.post("/api/v1/books", json=full_book_create_payload_copy,
                headers={"Authorization": bearer_token})

    api_response = client.get("/api/v1/books", headers={"Authorization": bearer_token})

    assert api_response.status_code == 200
    books = api_response.json()["data"]["books"]
    assert len(books) == 2


def test_validation_failing_if_invalid_book_id_in_fetch_book_by_id(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    provided_book_id = 2
    response = client.get(f"/api/v1/books/{provided_book_id}", headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_getting_book_by_id_api(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"

    # first book created
    first_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                      headers={"Authorization": bearer_token})
    first_book_response_book_id = first_book_response.json()["data"]["id"]

    full_book_create_payload_copy = full_book_create_payload.copy()
    full_book_create_payload_copy["title"] = "Second Book"

    # second book created
    second_book_response = client.post("/api/v1/books", json=full_book_create_payload_copy,
                                       headers={"Authorization": bearer_token})
    second_book_response_book_id = second_book_response.json()["data"]["id"]

    first_book_api_response = client.get(f"/api/v1/books/{first_book_response_book_id}",
                                         headers={"Authorization": bearer_token})

    assert first_book_api_response.status_code == 200
    assert first_book_api_response.json()["data"]["title"] == "My first book"

    second_book_api_response = client.get(f"/api/v1/books/{second_book_response_book_id}",
                                          headers={"Authorization": bearer_token})

    assert second_book_api_response.status_code == 200
    assert second_book_api_response.json()["data"]["title"] == "Second Book"


def test_validation_failing_if_review_text_missing_add_review(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})

    book_id = create_book_response.json()["data"]["id"]

    full_review_create_payload_copy = full_review_create_payload.copy()
    del full_review_create_payload_copy["review_text"]

    api_response = client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy,
                               headers={"Authorization": bearer_token})
    assert api_response.status_code == 422


def test_validation_failing_if_rating_less_than_0_add_review(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})

    book_id = create_book_response.json()["data"]["id"]

    full_review_create_payload_copy = full_review_create_payload.copy()
    full_review_create_payload_copy["rating"] = -2

    api_response = client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy,
                               headers={"Authorization": bearer_token})
    assert api_response.status_code == 400


def test_validation_failing_if_rating_missing_add_review(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})

    book_id = create_book_response.json()["data"]["id"]

    full_review_create_payload_copy = full_review_create_payload.copy()
    del full_review_create_payload_copy["rating"]

    api_response = client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy,
                               headers={"Authorization": bearer_token})
    assert api_response.status_code == 422


def test_validation_failing_if_invalid_book_id_in_add_reviews_to_book_by_id(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    provided_book_id = 2
    response = client.post(f"/api/v1/books/{provided_book_id}/reviews", json=full_review_create_payload,
                           headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_validation_failing__for_add_review_api_if_user_already_left_review_for_book(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload,
                headers={"Authorization": bearer_token})

    full_review_create_payload_copy = full_review_create_payload.copy()
    full_review_create_payload_copy["rating"] = 4
    full_review_create_payload_copy["review_text"] = "resubmitting my review"

    api_response = client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy,
                               headers={"Authorization": bearer_token})
    assert api_response.status_code == 400


def test_review_creation_if_proper_payload_provided(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    api_response = client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload,
                               headers={"Authorization": bearer_token})

    assert api_response.status_code == 201
    assert api_response.json()["data"]["id"] == 1
    assert api_response.json()["data"]["book_id"] == 1
    assert api_response.json()["data"]["user_id"] == 1
    assert session.query(Book).count() == 1
    assert session.query(Review).count() == 1


def test_validation_failing_if_invalid_book_id_in_get_summary_and_avg_ratings_of_book_by_id(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    provided_book_id = 2
    response = client.get(f"/api/v1/books/{provided_book_id}/summary", headers={"Authorization": bearer_token})
    assert response.status_code == 400


def test_get_summary_avg_rating_api_if_proper_payload_provided(client, session):
    bearer_token = f"Bearer {get_token(client=client)}"
    create_book_response = client.post("/api/v1/books", json=full_book_create_payload,
                                       headers={"Authorization": bearer_token})
    book_id = create_book_response.json()["data"]["id"]

    # Review 1
    client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload,
                headers={"Authorization": bearer_token})

    # Review 2
    full_register_payload_copy_one = full_register_payload.copy()
    full_register_payload_copy_one["email"] = "b@dummy.com"
    full_register_payload_copy_one["name"] = "dhaval 2"
    full_login_payload_copy_one = full_login_payload.copy()
    full_login_payload_copy_one["email"] = "b@dummy.com"
    full_review_create_payload_copy_one = full_review_create_payload.copy()
    full_review_create_payload_copy_one["rating"] = 4
    bearer_token = f"Bearer {get_token(client=client, register_payload=full_register_payload_copy_one, login_payload=full_login_payload_copy_one)}"
    client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy_one,
                headers={"Authorization": bearer_token})

    # Review 3
    full_register_payload_copy_two = full_register_payload.copy()
    full_register_payload_copy_two["email"] = "c@dummy.com"
    full_register_payload_copy_two["name"] = "dhaval 3"
    full_login_payload_copy_two = full_login_payload.copy()
    full_login_payload_copy_two["email"] = "c@dummy.com"
    full_review_create_payload_copy_two = full_review_create_payload.copy()
    full_review_create_payload_copy_two["rating"] = 3
    bearer_token = f"Bearer {get_token(client=client, register_payload=full_register_payload_copy_two, login_payload=full_login_payload_copy_two)}"
    client.post(f"/api/v1/books/{book_id}/reviews", json=full_review_create_payload_copy_two,
                headers={"Authorization": bearer_token})

    api_response = client.get(f"/api/v1/books/{book_id}/summary", headers={"Authorization": bearer_token})

    assert api_response.status_code == 200
    assert api_response.json()["data"]["book_id"] == 1
    assert api_response.json()["data"]["average_rating"] == 4
    assert session.query(Review).count() == 3
