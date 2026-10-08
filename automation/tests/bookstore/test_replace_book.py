# tests/bookstore/test_replace_book.py
# Tests for PUT /BookStore/v1/Books/{ISBN} (Replace Book in Collection): TC-022 to TC-024.

from config import ISBN_A, ISBN_B, ISBN_C, ISBN_INVALID
from helpers import isbns_in
import pytest


def test_tc022_replace_book_with_valid_isbn(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-022: Verify a book in the collection can be replaced with another valid book."""
    # `book_in_collection` has already put ISBN_A into this user's collection.
    response = books_api.replace_book(
        book_in_collection, new_user.user_id, ISBN_B, auth_token)

    assert response.status == 200
    # Follow-up read: ISBN_B has taken the place of ISBN_A.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_B]


@pytest.mark.negative
def test_tc023_replace_book_with_invalid_new_isbn_is_rejected(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-023: Verify the request fails when the new ISBN is invalid."""
    response = books_api.replace_book(
        book_in_collection, new_user.user_id, ISBN_INVALID, auth_token)

    assert response.status == 400
    # Follow-up read: the original book is still there, unchanged.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_A]


@pytest.mark.negative
def test_tc024_replace_book_not_in_collection_is_rejected(
    account_api, books_api, new_user, auth_token
):
    """TC-024: Verify the request fails when the book being replaced is not in the collection."""
    # This user has an empty collection, so ISBN_A is not in it.
    response = books_api.replace_book(
        ISBN_A, new_user.user_id, ISBN_C, auth_token)

    assert response.status == 400
    assert response.json()["code"] == "1206"
    # Follow-up read: the collection is still empty (ISBN_C was not added).
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == []
