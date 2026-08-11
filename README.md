# BookHub API Quality Assurance

Independent API testing project validating the BookHub (Book Store) REST API — covering user account
management, authentication, book catalogue operations, and user collection management.

## Overview

This project applies a full, disciplined test lifecycle to a real (public demo) REST API: requirement
analysis from Swagger/OpenAPI documentation, a written test plan with dependency mapping, 27 structured
test cases (positive, negative, business-rule, and security-oriented), full execution in Postman, one
confirmed defect, and a final closure report comparing planned vs. actual outcomes.

Portfolio presentation (narrative, scope, and links to all documents below) is hosted on Notion:
[View the full project on Notion](https://damilareakanni.notion.site/Damilare-A-014433797aa68349805181612bc6e1d9?source=copy_link)

## API Under Test

- **API:** BookHub (Book Store) API
- **Base URL:** `https://bookstore.toolsqa.com`
- **Documentation:** `https://bookstore.toolsqa.com/swagger/`

## Repository Structure

```
bookhub-api-testing/
├── README.md
├── postman/
│   ├── BookHub.postman_collection.json
│   └── BookHub.postman_environment.json
├── test-plan/
│   └── Test-Plan.md
├── test-cases/
│   └── Test-Case-Suite.md
├── defects/
│   └── Bug-Tracker.md
├── execution/
│   └── Test-Closure-Report.md
└── evidence/
    └── screenshots/
```

## Key Finding

**DEF-001 — JWT payload exposes plaintext password.** The token returned by `POST /Account/v1/GenerateToken`
contains the user's plaintext password in its (unencrypted, base64-encoded) payload. Full details in
[`defects/Bug-Tracker.md`](defects/Bug-Tracker.md).

## Execution Summary

| Metric | Count |
|---|---|
| Test cases planned | 27 |
| Test cases executed | 27 |
| Passed | 26 |
| Failed | 1 |
| Defects raised | 1 |

Full breakdown in [`execution/Test-Closure-Report.md`](execution/Test-Closure-Report.md).

## Tools

Postman (collection design, environment variables, request chaining, automated assertions), Swagger UI
(API documentation reference).

## Running This Collection

1. Import `postman/BookHub.postman_collection.json` and `postman/BookHub.postman_environment.json` into Postman.
2. Select the **BookHub - Dev** environment.
3. Set `baseUrl` to `https://bookstore.toolsqa.com` (pre-filled).
4. Run the collection via Collection Runner. Test credentials (`userName`, `password`) are generated
   automatically via a pre-request script on the Create User request — no manual setup required beyond
   `baseUrl`.

## Note on Credentials

No real API keys, tokens, or personal credentials are stored in this repository. All test credentials are
generated dynamically at runtime.
