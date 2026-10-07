# tests/account/test_authorize.py
# Tests for POST /Account/v1/Authorized (Authorize): TC-008 to TC-010.

from config import TEST_PASSWORD
from helpers import unique_username


def test_tc008_authorize_with_valid_credentials(account_api, new_user, auth_token):
    """TC-008: Verify authorization succeeds with valid credentials."""
    # `auth_token` is requested so a token exists for this user first.
    # A brand-new user without a token gets false; once a token has been
    # generated, valid credentials get true.
    response = account_api.authorize(new_user.user_name, new_user.password)

    assert response.status == 200
    # The body is the bare JSON value true, not an object.
    assert response.json() is True


def test_tc009_authorize_non_existent_user_fails(account_api):
    """TC-009: Verify authorization fails for a non-existent user."""
    # A freshly generated name cannot belong to any registered user.
    response = account_api.authorize(unique_username(), TEST_PASSWORD)

    assert response.status == 404


def test_tc010_authorize_wrong_password_fails(account_api, new_user):
    """TC-010: Verify authorization fails for an existing user with the wrong password."""
    response = account_api.authorize(new_user.user_name, "Wrong@Pass1")

    # The API answers 404 here too, the same as for a user that does not exist,
    # so the response does not reveal whether an account exists.
    assert response.status == 404
    assert response.json() is not True