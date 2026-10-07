# conftest.py
# Shared setup for the whole suite. pytest finds this file by name and makes
# everything defined in it available to every test automatically.

import uuid
from dataclasses import dataclass

import pytest
from playwright.sync_api import Playwright

from api.account import AccountAPI
from api.bookstore import BookStoreAPI
from config import BASE_URL

# A throwaway password for the users our tests create on the public demo API.
# It meets the API's password policy (upper, lower, digit, special, 8+ chars).
TEST_PASSWORD = "Test@1234"


@dataclass
class User:
    # A small container for the details of one test user.
    user_id: str
    user_name: str
    password: str


@pytest.fixture
def api_request(playwright: Playwright):
    # Create an API client that already knows the base address.
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context
    # Everything after `yield` runs when the test finishes, pass or fail.
    request_context.dispose()


@pytest.fixture
def books_api(api_request):
    # A BookStoreAPI object wired to the client above.
    return BookStoreAPI(api_request)


@pytest.fixture
def account_api(api_request):
    # An AccountAPI object wired to the same client.
    return AccountAPI(api_request)


@pytest.fixture
def new_user(account_api):
    # SETUP: create a brand-new user with a name no other test run will share.
    user_name = f"qa_{uuid.uuid4().hex[:10]}"
    response = account_api.create_user(user_name, TEST_PASSWORD)
    assert response.status == 201, f"Could not create test user: {response.status} {response.text()}"
    user = User(
        user_id=response.json()["userID"],
        user_name=user_name,
        password=TEST_PASSWORD,
    )

    yield user

    # TEARDOWN: runs after the test, even if the test failed.
    # Get a fresh token of our own, then delete the user.
    token = account_api.generate_token(
        user.user_name, user.password).json().get("token")
    if token:
        account_api.delete_user(user.user_id, token)
