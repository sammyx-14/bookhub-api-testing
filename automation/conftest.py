# conftest.py
# Shared setup for the whole suite. pytest finds this file by name and makes
# everything defined in it available to every test automatically.

from dataclasses import dataclass

import pytest
from playwright.sync_api import Playwright

from api.account import AccountAPI
from api.bookstore import BookStoreAPI
from config import BASE_URL, TEST_PASSWORD
from helpers import unique_username


@dataclass
class User:
    # A small container for the details of one test user.
    user_id: str
    user_name: str
    password: str


def delete_user_quietly(account_api, user_id, user_name, password):
    # Log in with a fresh token, then delete the user.
    # If the user is already gone, no token comes back and we simply do nothing.
    token = account_api.generate_token(user_name, password).json().get("token")
    if token:
        account_api.delete_user(user_id, token)


@pytest.fixture
def api_request(playwright: Playwright):
    # Create an API client that already knows the base address.
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()


@pytest.fixture
def books_api(api_request):
    return BookStoreAPI(api_request)


@pytest.fixture
def account_api(api_request):
    return AccountAPI(api_request)


@pytest.fixture
def new_user(account_api):
    # SETUP: create a brand-new user no other test run will share.
    user_name = unique_username()
    response = account_api.create_user(user_name, TEST_PASSWORD)
    assert response.status == 201, f"Could not create test user: {response.status} {response.text()}"
    user = User(
        user_id=response.json()["userID"],
        user_name=user_name,
        password=TEST_PASSWORD,
    )

    yield user

    # TEARDOWN: runs after the test, even if the test failed.
    delete_user_quietly(account_api, user.user_id, user.user_name, user.password)


@pytest.fixture
def auth_token(account_api, new_user):
    # A valid token for the test user from `new_user`.
    response = account_api.generate_token(new_user.user_name, new_user.password)
    token = response.json().get("token")
    assert token, f"Could not get a token for the test user: {response.text()}"
    return token


@pytest.fixture
def cleanup(account_api):
    # For tests that create a user THEMSELVES (so they can't use `new_user`).
    # The test registers each user it creates; the fixture deletes them afterwards.
    registered = []

    def register(user_id, user_name, password):
        registered.append((user_id, user_name, password))

    yield register

    for user_id, user_name, password in registered:
        delete_user_quietly(account_api, user_id, user_name, password)