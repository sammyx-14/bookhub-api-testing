# tests/account/test_delete_user.py
# Tests for DELETE /Account/v1/User/{UUID} (Delete User): TC-029 to TC-030.


def test_tc029_delete_user_without_token_is_rejected(account_api, new_user, auth_token):
    """TC-029: Verify the request fails when no token is attached."""
    # No token is passed to delete_user, so no Authorization header is sent.
    response = account_api.delete_user(new_user.user_id)

    assert response.status == 401
    # Follow-up read (using the user's real token): the user still exists.
    still_there = account_api.get_user(new_user.user_id, auth_token)
    assert still_there.status == 200


def test_tc030_delete_user_with_valid_token(account_api, new_user, auth_token):
    """TC-030: Verify a user can be deleted with a valid token."""
    response = account_api.delete_user(new_user.user_id, auth_token)

    assert response.status == 204
    # Follow-up read: the user is gone.
    gone = account_api.get_user(new_user.user_id, auth_token)
    assert gone.status == 401