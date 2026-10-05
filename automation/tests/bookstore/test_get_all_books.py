# tests/bookstore/test_get_all_books.py


def test_tc014_get_all_books_returns_catalogue(books_api):
    """TC-014: Verify the book catalogue is returned successfully."""
    # Act: ask the API for the full catalogue.
    response = books_api.get_all_books()

    # Assert: the status code is 200 (OK).
    assert response.status == 200

    body = response.json()

    # Assert: the catalogue is not empty.
    assert len(body["books"]) > 0

    # Assert: the first book has the fields the API documents.
    first_book = body["books"][0]
    assert "isbn" in first_book
    assert "title" in first_book