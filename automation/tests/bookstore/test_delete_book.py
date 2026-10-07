# tests/bookstore/test_delete_book.py
# Tests for DELETE /BookStore/v1/Book (Delete Book from Collection): TC-025 to TC-026.

from config import ISBN_A, ISBN_B
from helpers import isbns_in


def test_tc025_delete_book_in_collection(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-025: Verify a book in the collection can be deleted."""
    # `book_in_collection` has already put ISBN_A into this user's collection.
    response = books_api.delete_book(new_user.user_id, book_in_collection, auth_token)

    assert response.status == 204
    # Follow-up read: the collection is now empty.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == []


def test_tc026_delete_book_not_in_collection_is_rejected(
    account_api, books_api, new_user, auth_token, book_in_collection
):
    """TC-026: Verify the request fails when the book is not in the collection."""
    # The collection holds ISBN_A only, so ISBN_B is not in it.
    response = books_api.delete_book(new_user.user_id, ISBN_B, auth_token)

    assert response.status == 400
    assert response.json()["code"] == "1206"
    # Follow-up read: the existing book was not touched.
    user = account_api.get_user(new_user.user_id, auth_token).json()
    assert isbns_in(user) == [ISBN_A]