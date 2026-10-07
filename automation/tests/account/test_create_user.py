# tests/account/test_create_user.py
# Tests for POST /Account/v1/User (Create User): TC-001 to TC-004.

import pytest

from config import TEST_PASSWORD
from helpers import unique_username


def test_tc001_register_with_valid_credentials(account_api, cleanup):
    """TC-001: Verify user registration succeeds with a valid username and password."""
    user_name = unique_username()

    response = account_api.create_user(user_name, TEST_PASSWORD)

    assert response.status == 201
    body = response.json()
    # Register the new user for deletion straight away, so the cleanup
    # still happens even if one of the asserts below fails.
    cleanup(body["userID"], user_name, TEST_PASSWORD)
    assert body["username"] == user_name
    assert "password" not in body


def test_tc002_register_without_password_is_rejected(account_api):
    """TC-002: Verify registration fails when the password field is missing."""
    response = account_api.create_user(unique_username())  # no password sent

    assert response.status == 400
    body = response.json()
    assert body["code"] == "1200"
    assert body["message"]  # a non-empty error message is returned


def test_tc003_register_with_existing_username_is_rejected(account_api, new_user):
    """TC-003: Verify registration fails when the username already exists."""
    response = account_api.create_user(new_user.user_name, TEST_PASSWORD)

    assert response.status == 406
    assert response.json()["message"]


# Each password below breaks exactly one rule of the API's password policy
# (8+ characters, upper, lower, digit, special), except the first, which breaks them all.
WEAK_PASSWORDS = [
    pytest.param("abc", id="breaks-every-rule"),
    pytest.param("Abcde1!", id="seven-characters"),
    pytest.param("abcdef1!", id="no-uppercase"),
    pytest.param("ABCDEF1!", id="no-lowercase"),
    pytest.param("Abcdefg!", id="no-digit"),
    pytest.param("Abcdefg1", id="no-special-character"),
]


@pytest.mark.parametrize("password", WEAK_PASSWORDS)
def test_tc004_register_with_weak_password_is_rejected(account_api, password):
    """TC-004: Verify registration fails when the password breaks the password policy."""
    response = account_api.create_user(unique_username(), password)

    assert response.status == 400
    assert response.json()["code"] == "1300"


def test_tc004_boundary_eight_character_password_is_accepted(account_api, cleanup):
    """TC-004 boundary pair: 7 characters is rejected above, so a compliant
    8-character password must be accepted."""
    user_name = unique_username()
    password = "Abcdef1!"

    response = account_api.create_user(user_name, password)

    assert response.status == 201
    cleanup(response.json()["userID"], user_name, password)