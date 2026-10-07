# tests/account/test_get_user.py
# Tests for GET /Account/v1/User/{UUID} (Get User): TC-011 to TC-013.


def test_tc011_get_user_with_valid_uuid_and_token(account_api, new_user, auth_token):
    """TC-011: Verify user details are returned for a valid UUID with a valid token."""
    response = account_api.get_user(new_user.user_id, auth_token)

    assert response.status == 200
    body = response.json()
    # Note the casing: this endpoint returns "userId", while Create User returns "userID".
    assert body["userId"] == new_user.user_id
    assert body["username"] == new_user.user_name
    # A brand-new user has no books yet.
    assert body["books"] == []


def test_tc012_get_user_without_token_is_rejected(account_api, new_user):
    """TC-012: Verify the request fails when no token is attached."""
    response = account_api.get_user(new_user.user_id)  # no token sent

    assert response.status == 401


def test_tc013_get_user_with_non_existent_uuid_is_rejected(account_api, auth_token):
    """TC-013: Verify the request fails for a non-existent UUID."""
    # An all-zero UUID is well-formed but cannot belong to any registered user.
    response = account_api.get_user("00000000-0000-0000-0000-000000000000", auth_token)

    assert response.status == 401