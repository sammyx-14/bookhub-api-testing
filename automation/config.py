# config.py
# One place for the settings the whole test suite shares.

BASE_URL = "https://bookstore.toolsqa.com"

# Throwaway password for the users our tests create on the public demo API.
# It meets the API's password policy (upper, lower, digit, special, 8+ chars).
TEST_PASSWORD = "Test@1234"

# Four real books from the catalogue (the same ones the Postman collection used),
# plus one ISBN that exists nowhere. Tests use the names, never the raw numbers.
ISBN_A = "9781449325862"
ISBN_B = "9781449331818"
ISBN_C = "9781449365035"
ISBN_D = "9781491904244"
ISBN_INVALID = "0000000000000"