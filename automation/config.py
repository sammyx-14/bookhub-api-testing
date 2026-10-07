# config.py
# One place for the settings the whole test suite shares.

BASE_URL = "https://bookstore.toolsqa.com"

# Throwaway password for the users our tests create on the public demo API.
# It meets the API's password policy (upper, lower, digit, special, 8+ chars).
TEST_PASSWORD = "Test@1234"