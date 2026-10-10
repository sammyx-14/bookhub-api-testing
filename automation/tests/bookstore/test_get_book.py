# tests/bookstore/test_get_book.py
# Tests for GET /BookStore/v1/Book?ISBN=... (Get Book): TC-015 to TC-016.

import pytest
from config import ISBN_A, ISBN_INVALID
from schemas import BOOK, assert_schema


def test_tc015_get_book_with_valid_isbn(books_api):
    """TC-015: Verify a single book is returned for a valid ISBN."""
    response = books_api.get_book(ISBN_A)

    assert response.status == 200
    body = response.json()
    assert_schema(body, BOOK)
    assert body["isbn"] == ISBN_A
    assert body["title"] == "Git Pocket Guide"


@pytest.mark.negative
def test_tc016_get_book_with_invalid_isbn_is_rejected(books_api):
    """TC-016: Verify the request fails for an invalid ISBN."""
    response = books_api.get_book(ISBN_INVALID)

    assert response.status == 400
