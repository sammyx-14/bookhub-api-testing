# conftest.py
# Shared setup for the whole suite. pytest finds this file by name and makes
# everything defined in it available to every test automatically.

import pytest
from playwright.sync_api import Playwright

from api.bookstore import BookStoreAPI
from config import BASE_URL


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