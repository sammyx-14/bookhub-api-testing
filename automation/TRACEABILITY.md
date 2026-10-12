# Traceability: test case ID to automated test

Generated from the test code by `make_traceability.py`. Each row links a test
case ID (as used in the Test Cases document) to the pytest function that checks it.

| ID | What it verifies | Test function | File | Markers |
|---|---|---|---|---|
| TC-001 | Verify user registration succeeds with a valid username and password. | `test_tc001_register_with_valid_credentials` | `tests/account/test_create_user.py` | - |
| TC-002 | Verify registration fails when the password field is missing. | `test_tc002_register_without_password_is_rejected` | `tests/account/test_create_user.py` | negative |
| TC-003 | Verify registration fails when the username already exists. | `test_tc003_register_with_existing_username_is_rejected` | `tests/account/test_create_user.py` | negative |
| TC-004 | Verify registration fails when the password breaks the password policy. | `test_tc004_register_with_weak_password_is_rejected` | `tests/account/test_create_user.py` | negative |
| TC-004 | Verify registration succeeds with a password of exactly 8 characters (boundary). | `test_tc004_boundary_eight_character_password_is_accepted` | `tests/account/test_create_user.py` | - |
| TC-005 | Verify token generation succeeds with valid credentials. | `test_tc005_generate_token_with_valid_credentials` | `tests/account/test_generate_token.py` | - |
| TC-006 | Verify the response indicates failure when the password is incorrect. | `test_tc006_generate_token_with_wrong_password_fails` | `tests/account/test_generate_token.py` | negative, security |
| TC-007 | Verify the JWT payload does not expose sensitive credentials. | `test_tc007_jwt_payload_excludes_password` | `tests/account/test_generate_token.py` | security |
| TC-008 | Verify authorization succeeds with valid credentials. | `test_tc008_authorize_with_valid_credentials` | `tests/account/test_authorize.py` | - |
| TC-009 | Verify authorization fails for a non-existent user. | `test_tc009_authorize_non_existent_user_fails` | `tests/account/test_authorize.py` | negative, security |
| TC-010 | Verify authorization fails for an existing user with the wrong password. | `test_tc010_authorize_wrong_password_fails` | `tests/account/test_authorize.py` | negative, security |
| TC-011 | Verify user details are returned for a valid UUID with a valid token. | `test_tc011_get_user_with_valid_uuid_and_token` | `tests/account/test_get_user.py` | - |
| TC-012 | Verify the request fails when no token is attached. | `test_tc012_get_user_without_token_is_rejected` | `tests/account/test_get_user.py` | negative, security |
| TC-013 | Verify the request fails for a non-existent UUID. | `test_tc013_get_user_with_non_existent_uuid_is_rejected` | `tests/account/test_get_user.py` | negative |
| TC-014 | Verify the book catalogue is returned successfully. | `test_tc014_get_all_books_returns_catalogue` | `tests/bookstore/test_get_all_books.py` | - |
| TC-015 | Verify a single book is returned for a valid ISBN. | `test_tc015_get_book_with_valid_isbn` | `tests/bookstore/test_get_book.py` | - |
| TC-016 | Verify the request fails for an invalid ISBN. | `test_tc016_get_book_with_invalid_isbn_is_rejected` | `tests/bookstore/test_get_book.py` | negative |
| TC-017 | Verify a valid book can be added to a user's collection. | `test_tc017_add_book_with_valid_isbn` | `tests/bookstore/test_add_book.py` | - |
| TC-018 | Verify the request fails when the ISBN is invalid. | `test_tc018_add_book_with_invalid_isbn_is_rejected` | `tests/bookstore/test_add_book.py` | negative |
| TC-019 | Verify the request fails when no token is attached. | `test_tc019_add_book_without_token_is_rejected` | `tests/bookstore/test_add_book.py` | negative, security |
| TC-020 | Verify the request fails when the ISBN is already in the user's collection. | `test_tc020_add_duplicate_isbn_is_rejected` | `tests/bookstore/test_add_book.py` | negative |
| TC-021 | Verify one user cannot add a book to another user's collection. | `test_tc021_cannot_add_book_to_another_users_collection` | `tests/bookstore/test_add_book.py` | negative, security |
| TC-022 | Verify a book in the collection can be replaced with another valid book. | `test_tc022_replace_book_with_valid_isbn` | `tests/bookstore/test_replace_book.py` | - |
| TC-023 | Verify the request fails when the new ISBN is invalid. | `test_tc023_replace_book_with_invalid_new_isbn_is_rejected` | `tests/bookstore/test_replace_book.py` | negative |
| TC-024 | Verify the request fails when the book being replaced is not in the collection. | `test_tc024_replace_book_not_in_collection_is_rejected` | `tests/bookstore/test_replace_book.py` | negative |
| TC-025 | Verify a book in the collection can be deleted. | `test_tc025_delete_book_in_collection` | `tests/bookstore/test_delete_book.py` | - |
| TC-026 | Verify the request fails when the book is not in the collection. | `test_tc026_delete_book_not_in_collection_is_rejected` | `tests/bookstore/test_delete_book.py` | negative |
| TC-027 | Verify the request fails when no token is attached. | `test_tc027_delete_all_books_without_token_is_rejected` | `tests/bookstore/test_delete_all_books.py` | negative, security |
| TC-028 | Verify all books are removed from the collection with a valid token. | `test_tc028_delete_all_books_with_valid_token` | `tests/bookstore/test_delete_all_books.py` | - |
| TC-029 | Verify the request fails when no token is attached. | `test_tc029_delete_user_without_token_is_rejected` | `tests/account/test_delete_user.py` | negative, security |
| TC-030 | Verify a user can be deleted with a valid token. | `test_tc030_delete_user_with_valid_token` | `tests/account/test_delete_user.py` | - |
| E2E-001 | Verify the full user journey: register, token, add, replace, delete book, delete user. | `test_e2e001_full_user_lifecycle` | `tests/e2e/test_e2e_lifecycle.py` | e2e |

32 test functions. TC-004 is covered by two functions (the weak-password set and the 8-character boundary).
