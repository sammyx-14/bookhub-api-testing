# conftest.py
# Shared setup for the whole suite. pytest finds this file by name and makes
# everything defined in it available to every test automatically.

from dataclasses import dataclass
import allure
import pytest
from playwright.sync_api import Playwright

from api.account import AccountAPI
from api.bookstore import BookStoreAPI
from config import BASE_URL, ISBN_A, TEST_PASSWORD
from helpers import unique_username


@dataclass
class User:
    # A small container for the details of one test user.
    user_id: str
    user_name: str
    password: str


def create_test_user(account_api):
    # Register a brand-new user with a name no other test run will share.
    user_name = unique_username()
    response = account_api.create_user(user_name, TEST_PASSWORD)
    assert response.status == 201, f"Could not create test user: {response.status} {response.text()}"
    return User(
        user_id=response.json()["userID"],
        user_name=user_name,
        password=TEST_PASSWORD,
    )


def delete_user_if_exists(account_api, user_id, user_name, password):
    # Log in with a fresh token, then delete the user.
    # If the user is already gone (a test deleted it), no token comes back and we skip.
    token = account_api.generate_token(user_name, password).json().get("token")
    if token:
        response = account_api.delete_user(user_id, token)
        # A failed cleanup must be visible, never silent.
        assert response.status == 204, (
            f"Cleanup failed for {user_name}: {response.status} {response.text()}"
        )


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
    # SETUP: create a brand-new user.
    user = create_test_user(account_api)

    yield user

    # TEARDOWN: runs after the test, even if the test failed.
    delete_user_if_exists(account_api, user.user_id,
                          user.user_name, user.password)


@pytest.fixture
def other_user(account_api):
    # A SECOND, independent user, for tests that involve two people (TC-021).
    user = create_test_user(account_api)

    yield user

    delete_user_if_exists(account_api, user.user_id,
                          user.user_name, user.password)


@pytest.fixture
def auth_token(account_api, new_user):
    # A valid token for the test user from `new_user`.
    response = account_api.generate_token(
        new_user.user_name, new_user.password)
    token = response.json().get("token")
    assert token, f"Could not get a token for the test user: {response.text()}"
    return token


@pytest.fixture
def book_in_collection(books_api, new_user, auth_token):
    # Puts one known book (ISBN_A) into the test user's collection and returns its ISBN.
    # No teardown needed: deleting the user also removes their collection.
    response = books_api.add_books(new_user.user_id, [ISBN_A], auth_token)
    assert response.status == 201, f"Could not add the starting book: {response.status} {response.text()}"
    return ISBN_A


@pytest.fixture
def cleanup(account_api):
    # For tests that create a user THEMSELVES (so they can't use `new_user`).
    # The test registers each user it creates; the fixture deletes them afterwards.
    registered = []

    def register(user_id, user_name, password):
        registered.append((user_id, user_name, password))

    yield register

    for user_id, user_name, password in registered:
        delete_user_if_exists(account_api, user_id, user_name, password)


# --- Allure labelling -------------------------------------------------------
# One hook that labels every test in the report, so the 37 tests need no
# Allure decorators of their own. It reads the markers we already attach.


def pytest_collection_modifyitems(items):
    # pytest calls this once, after it has found all the tests.
    for item in items:
        # Feature: from the file name, e.g. test_add_book.py -> "Add Book".
        file_stem = item.path.stem.removeprefix("test_")
        feature = file_stem.replace("_", " ").title()
        item.add_marker(allure.feature(feature))

        # Severity: from the markers the test already carries.
        if item.get_closest_marker("e2e"):
            severity = allure.severity_level.BLOCKER
        elif item.get_closest_marker("security"):
            severity = allure.severity_level.CRITICAL
        else:
            severity = allure.severity_level.NORMAL
        item.add_marker(allure.severity(severity))

