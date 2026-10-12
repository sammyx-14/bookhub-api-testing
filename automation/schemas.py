# schemas.py
# The "contract" for the API's key responses: which fields must exist and
# what type each one is. Built from real responses captured on 10 Oct 2026.
# Values are not checked here (the tests do that); only the shape is.

from jsonschema import validate


def assert_schema(body, schema):
    # Raises a clear error naming the exact field that broke the contract.
    validate(instance=body, schema=schema)


# One book. The same shape appears in Get Book, Get All Books and Get User.
BOOK = {
    "type": "object",
    "required": [
        "isbn", "title", "subTitle", "author", "publish_date",
        "publisher", "pages", "description", "website",
    ],
    "properties": {
        "isbn": {"type": "string"},
        "title": {"type": "string"},
        "subTitle": {"type": "string"},
        "author": {"type": "string"},
        "publish_date": {"type": "string"},
        "publisher": {"type": "string"},
        "pages": {"type": "integer"},
        "description": {"type": "string"},
        "website": {"type": "string"},
    },
}

# POST /Account/v1/User  (note the capital D in "userID")
CREATE_USER = {
    "type": "object",
    "required": ["userID", "username", "books"],
    "properties": {
        "userID": {"type": "string"},
        "username": {"type": "string"},
        "books": {"type": "array"},
    },
}

# POST /Account/v1/GenerateToken (successful login)
TOKEN = {
    "type": "object",
    "required": ["token", "expires", "status", "result"],
    "properties": {
        "token": {"type": "string"},
        "expires": {"type": "string"},
        "status": {"type": "string"},
        "result": {"type": "string"},
    },
}

# GET /Account/v1/User/{UUID}  (note the lowercase d in "userId")
GET_USER = {
    "type": "object",
    "required": ["userId", "username", "books"],
    "properties": {
        "userId": {"type": "string"},
        "username": {"type": "string"},
        "books": {"type": "array", "items": BOOK},
    },
}

# GET /BookStore/v1/Books
GET_ALL_BOOKS = {
    "type": "object",
    "required": ["books"],
    "properties": {
        "books": {"type": "array", "items": BOOK},
    },
}