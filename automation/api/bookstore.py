# api/bookstore.py
# The "API layer" for the BookStore endpoints (/BookStore/v1/...).
# Tests call these methods instead of writing URLs themselves.


class BookStoreAPI:
    def __init__(self, request):
        # `request` is Playwright's request object: the thing that sends HTTP calls.
        self.request = request

    def get_all_books(self):
        # GET /BookStore/v1/Books  ->  returns the whole book catalogue.
        return self.request.get("/BookStore/v1/Books")