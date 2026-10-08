# E2E-001: one complete user journey, from registration to account deletion.

import pytest
from config import TEST_PASSWORD, ISBN_A, ISBN_B
from helpers import unique_username, isbns_in


@pytest.mark.e2e
def test_e2e001_full_user_lifecycle(account_api, books_api, cleanup):
    """E2E-001: Verify the whole journey works in sequence: register, get a token,
    add a book, replace it, delete it, then delete the user."""
    user_name = unique_username()

    # Stage 1: register a new user.
    created = account_api.create_user(user_name, TEST_PASSWORD)
    assert created.status == 201
    user_id = created.json()["userID"]
    # Register for cleanup straight away, so a failure in a later stage
    # still removes the user. If the test deletes the user itself (stage 6),
    # the cleanup sees it is already gone and skips it.
    cleanup(user_id, user_name, TEST_PASSWORD)

    # Stage 2: generate a token. Done once only, because a new token
    # invalidates the previous one.
    token_response = account_api.generate_token(user_name, TEST_PASSWORD)
    assert token_response.status == 200
    token = token_response.json()["token"]

    # Stage 3: add a book, then read the collection to prove it is there.
    added = books_api.add_books(user_id, [ISBN_A], token)
    assert added.status == 201
    user = account_api.get_user(user_id, token).json()
    assert isbns_in(user) == [ISBN_A]

    # Stage 4: replace that book with another one.
    replaced = books_api.replace_book(ISBN_A, user_id, ISBN_B, token)
    assert replaced.status == 200
    user = account_api.get_user(user_id, token).json()
    assert isbns_in(user) == [ISBN_B]

    # Stage 5: delete the book, leaving an empty collection.
    deleted_book = books_api.delete_book(user_id, ISBN_B, token)
    assert deleted_book.status == 204
    user = account_api.get_user(user_id, token).json()
    assert isbns_in(user) == []

    # Stage 6: delete the user, then prove the account is gone.
    deleted_user = account_api.delete_user(user_id, token)
    assert deleted_user.status == 204
    gone = account_api.get_user(user_id, token)
    assert gone.status == 401