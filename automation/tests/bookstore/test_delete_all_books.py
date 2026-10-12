# tests/bookstore/test_delete_all_books.py
# Tests for DELETE /BookStore/v1/Books?UserId=... (Delete All Books): TC-027 to TC-028.

import pytest
from config import ISBN_A
from helpers import isbns_in


@pytest.mark.negative
@pytest.mark.security
def test_tc027_delete_all_books_without_token_is_rejected(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-027: Verify the request fails when no token is attached."""
    # No token is passed to delete_all_books, so no Authorization header is sent.
    response = books_api.delete_all_books(new_user.user_id)

    assert response.status == 401
    # Follow-up read (using the user's real token): the collection is untouched.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_A]


def test_tc028_delete_all_books_with_valid_token(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-028: Verify all books are removed from the collection with a valid token."""
    response = books_api.delete_all_books(new_user.user_id, auth_token)

    assert response.status == 204
    # Follow-up read: the collection is now empty.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == []
