# api/bookstore.py
# The "API layer" for the BookStore endpoints (/BookStore/v1/...).
# Tests call these methods instead of writing URLs themselves.

from api.headers import bearer


class BookStoreAPI:
    def __init__(self, request):
        # `request` is Playwright's request object: the thing that sends HTTP calls.
        self.request = request

    def get_all_books(self):
        # GET /BookStore/v1/Books  ->  the whole book catalogue.
        return self.request.get("/BookStore/v1/Books")

    def get_book(self, isbn):
        # GET /BookStore/v1/Book?ISBN=...  ->  one book from the catalogue.
        return self.request.get("/BookStore/v1/Book", params={"ISBN": isbn})

    def add_books(self, user_id, isbns, token=None):
        # POST /BookStore/v1/Books  ->  adds one or more books to a user's collection.
        body = {
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns],
        }
        return self.request.post("/BookStore/v1/Books", data=body, headers=bearer(token))

    def replace_book(self, current_isbn, user_id, new_isbn, token=None):
        # PUT /BookStore/v1/Books/{ISBN}  ->  swaps one book in the collection for another.
        return self.request.put(
            f"/BookStore/v1/Books/{current_isbn}",
            data={"userId": user_id, "isbn": new_isbn},
            headers=bearer(token),
        )

    def delete_book(self, user_id, isbn, token=None):
        # DELETE /BookStore/v1/Book  ->  removes one book (the details go in the body).
        return self.request.delete(
            "/BookStore/v1/Book",
            data={"isbn": isbn, "userId": user_id},
            headers=bearer(token),
        )

    def delete_all_books(self, user_id, token=None):
        # DELETE /BookStore/v1/Books?UserId=...  ->  empties a user's collection.
        return self.request.delete(
            "/BookStore/v1/Books",
            params={"UserId": user_id},
            headers=bearer(token),
        )