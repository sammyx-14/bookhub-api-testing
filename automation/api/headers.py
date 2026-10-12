# api/headers.py
# Small helper shared by the Account and BookStore API classes.


def bearer(token):
    # The headers for an authenticated request.
    # With no token we send no Authorization header at all, which is how the
    # "no token" tests reach the API.
    return {"Authorization": f"Bearer {token}"} if token else {}