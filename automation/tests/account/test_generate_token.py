# tests/account/test_generate_token.py
# Tests for POST /Account/v1/GenerateToken (Generate Token): TC-005 to TC-007.

import base64
import json
import pytest


def decode_jwt_payload(token):
    # A JWT is three parts joined by dots: header.payload.signature.
    # The payload is only base64-encoded (not encrypted), so anyone can read it.
    payload = token.split(".")[1]
    # restore the trailing "=" padding base64 needs
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def test_tc005_generate_token_with_valid_credentials(account_api, new_user):
    """TC-005: Verify token generation succeeds with valid credentials."""
    response = account_api.generate_token(
        new_user.user_name, new_user.password)

    assert response.status == 200
    body = response.json()
    assert body["token"]
    assert body["expires"]
    assert body["status"] == "Success"
    assert body["result"] == "User authorized successfully."


@pytest.mark.negative
@pytest.mark.security
def test_tc006_generate_token_with_wrong_password_fails(account_api, new_user):
    """TC-006: Verify the response indicates failure when the password is incorrect."""
    response = account_api.generate_token(new_user.user_name, "Wrong@Pass1")

    # The API answers 200 even for a failed login; the failure shows only in the body.
    assert response.status == 200
    body = response.json()
    assert body["token"] is None
    assert body["status"] == "Failed"
    assert body["result"] == "User authorization failed."


@pytest.mark.security
@pytest.mark.xfail(strict=True, reason="DEF-001: the JWT payload exposes the plaintext password")
def test_tc007_jwt_payload_excludes_password(account_api, new_user):
    """TC-007: Verify the JWT payload does not expose sensitive credentials."""
    response = account_api.generate_token(
        new_user.user_name, new_user.password)
    token = response.json()["token"]

    payload = decode_jwt_payload(token)

    assert "password" not in payload
