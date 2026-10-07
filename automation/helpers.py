# helpers.py
# Small reusable functions used by the fixtures and the tests.

import uuid


def unique_username():
    # A random name, so test users never collide on the shared demo server.
    return f"qa_{uuid.uuid4().hex[:10]}"


def isbns_in(user_body):
    # The ISBNs in a user's collection, taken from a Get User response body.
    return [book["isbn"] for book in user_body["books"]]