# BookHub API — Bug Tracker

*Identified issues are documented to a standard that would allow a development team to understand,
reproduce, and act on them.*

| Defect ID | Title | Environment | Endpoint / Method | Preconditions | Steps to Reproduce | Expected Result | Actual Result | Priority | Status | Linked Test Case | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DEF-001 | JWT payload exposes plaintext password | BookHub API — public demo environment (`https://bookstore.toolsqa.com`) | `POST /Account/v1/GenerateToken` | A registered user exists with known credentials. | 1) Send `POST /Account/v1/GenerateToken` with valid `userName`/`password` 2) Capture the `token` value from the response 3) Split the token string on `.` to isolate the second segment (payload) 4) Base64-decode that segment | Token payload should contain only non-sensitive claims (e.g. `userId`, `iat`, `exp`) — no password, in any form. | Decoded token payload contains the plaintext password, in addition to the username and issued-at timestamp. | High | Open — Not Actionable (Third-Party API, No Dev Access) | TC-006 | JWTs are signed, not encrypted — the payload is trivially readable by anyone holding the token (browser dev tools, logs, proxies, network traffic), with no special tooling required beyond a standard base64 decoder. |

## Documentation Accuracy Notes

*Discrepancies between Swagger documentation and actual API behaviour, observed during execution — none
affect functional correctness.*

| Area | Documented (Swagger) | Actual Behaviour | Why It Matters |
|---|---|---|---|
| Create User response field | `userId` | `userID` | Field casing is inconsistent even within the same API, not just against the docs — a client can't assume one name across endpoints |
| Get User response field | `userId` | `userId` | Differs in casing from Create User's own response, despite representing the same field |
| Error response `code` field type | Number | String | Client code expecting a number for comparisons would need type coercion to avoid silent bugs |
| Delete User success status | 200 | 204 | Arguably more correct than documented — 204 is the proper REST convention for a delete with no response body |
| Generate Token with wrong credentials | Not specified as 200 | 200, with failure indicated via body fields only | Breaks the standard convention of using 401 for auth failures — functionally fine, but means a client can't rely on status code alone to detect failure |
