# tests/bookstore/test_add_book.py
# Tests for POST /BookStore/v1/Books (Add Book to Collection): TC-017 to TC-021.

from config import ISBN_A, ISBN_B, ISBN_INVALID
from helpers import isbns_in


def test_tc017_add_book_with_valid_isbn(account_api, books_api, new_user, auth_token):
    """TC-017: Verify a valid book can be added to a user's collection."""
    response = books_api.add_books(new_user.user_id, [ISBN_A], auth_token)

    assert response.status == 201
    # Follow-up read: prove the book is really in the collection.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_A]


def test_tc018_add_book_with_invalid_isbn_is_rejected(account_api, books_api, new_user, auth_token):
    """TC-018: Verify the request fails when the ISBN is invalid."""
    response = books_api.add_books(new_user.user_id, [ISBN_INVALID], auth_token)

    assert response.status == 400
    # Follow-up read: nothing was added.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == []


def test_tc019_add_book_without_token_is_rejected(account_api, books_api, new_user, auth_token):
    """TC-019: Verify the request fails when no token is attached."""
    # No token is passed to add_books, so no Authorization header is sent.
    response = books_api.add_books(new_user.user_id, [ISBN_B])

    assert response.status == 401
    # Follow-up read (using the user's real token): nothing was added.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == []


def test_tc020_add_duplicate_isbn_is_rejected(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-020: Verify the request fails when the ISBN is already in the user's collection."""
    # `book_in_collection` has already put ISBN_A into this user's collection.
    response = books_api.add_books(new_user.user_id, [book_in_collection], auth_token)

    assert response.status == 400
    assert response.json()["code"] == "1210"
    # Follow-up read: still exactly one copy.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_A]


def test_tc021_cannot_add_book_to_another_users_collection(
    account_api, books_api, new_user, auth_token, other_user
):
    """TC-021: Verify one user cannot add a book to another user's collection."""
    # User A (new_user) tries to add a book to user B (other_user), using A's own token.
    response = books_api.add_books(other_user.user_id, [ISBN_A], auth_token)

    assert response.status == 401
    # Follow-up read as user B: B's collection is untouched.
    other_token = account_api.generate_token(other_user.user_name, other_user.password).json()["token"]
    other = account_api.get_user(other_user.user_id, other_token).json()
    assert isbns_in(other) == []