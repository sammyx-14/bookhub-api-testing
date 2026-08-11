# BookHub API — Test Plan

## 1. Objective

Validate the core functionality of the BookHub (Book Store) REST API — user account management,
authentication, and book catalogue/collection operations — to confirm the API behaves according to its
documented contract (Swagger), handles invalid and boundary input safely, and maintains data integrity
across dependent operations (e.g. a book correctly appearing in a user's collection after being added).

## 2. Scope

### In Scope

- **Account & Authentication** — user registration, token generation, credential authorization, invalid/missing credential handling
- **Book Catalogue** — retrieving available books, retrieving a single book by ISBN
- **User Collection Management** — adding books to a user's collection, replacing a book via ISBN, verifying collection state, removing individual or all books from a collection
- **User Lifecycle** — user retrieval by ID, user deletion, and the effect of deletion on associated collection data
- **Negative & Error Handling** — invalid payloads, missing required fields, non-existent resource IDs, unauthorized/unauthenticated requests, duplicate registration attempts
- **Boundary Conditions** — limits on fields where the API or observed behaviour defines a meaningful constraint

### Out of Scope

- Performance / load testing
- Active security/penetration testing (basic credential-handling checks within documented endpoints —
  e.g. verifying sensitive data isn't exposed in responses — are included as part of standard contract validation)
- UI-layer testing (the DemoQA front end is referenced only for business-flow context, not tested directly)

## 3. Test Approach / Strategy

- **Testing type:** Black-box API testing — validating behaviour and response contracts without inspecting server-side implementation.
- **Tooling:** Postman, using a structured collection with environment variables and request chaining to propagate `userId` and `token` across dependent requests rather than hardcoding values.
- **Test design:** Positive, negative, boundary, and basic security/data-handling test cases derived directly from the documented request/response models (`RegisterViewModel`, `LoginViewModel`, `AddListOfBooks`, `ReplaceIsbn`, etc.).
- **Assertions:** Beyond status code — response body structure and values are validated against the documented model shape (e.g. confirming `CreateUserResult` does not return a password field).
- **Prioritization:** Risk-based. Higher-value test cases (e.g. auth failures, data integrity after write operations) are prioritized; exhaustive field-permutation testing is deliberately avoided in favour of depth on meaningful cases.
- **Execution order:** Dependency-aware — see Section 7.

## 4. Test Environment

| Item | Detail |
|---|---|
| API under test | BookHub (Book Store) API |
| Base URL | `https://bookstore.toolsqa.com` |
| Documentation | `https://bookstore.toolsqa.com/swagger/` |
| Tooling | Postman (collection + environment), Swagger UI (reference) |
| Environment type | Public shared demo environment (not a dedicated/isolated test instance) |

## 5. Entry Criteria

- API is reachable and Swagger documentation has been reviewed.
- Full endpoint list confirmed (method, path, purpose) for both Account and BookStore resources.
- Request/response model shapes confirmed for all endpoints in scope.
- Dependency chain between endpoints mapped (see Section 7).
- Postman collection and environment variables are set up and ready for use.

## 6. Exit Criteria

- All planned test cases have been executed and results recorded (pass / fail / blocked).
- All identified defects have been logged, with priority assigned and justified.
- Critical and high-severity defects have been re-verified against current live API behaviour. As this
  project targets a third-party public API with no development access, formal fix-and-retest was not
  applicable within project scope.
- A final execution/coverage summary has been produced.
- Known limitations and untested areas are explicitly documented rather than implied to be covered.

## 7. Dependencies & Execution Order

Testing follows the real data dependency chain rather than an arbitrary order, since several operations
require state created by a prior request. If a prerequisite step fails, all downstream steps are expected
to fail as a consequence of that dependency — not treated as independent defects.

| Request | Dependency | Order (Request) | Execution Flow (with Verification) |
|---|---|---|---|
| Create User | None | Create User | Create User |
| Generate Token | Create User | Generate Token | Generate Token → Authorize |
| Authorize | Create User | Authorize | Get User |
| Get User | Generate Token | Get User | Get All Books |
| Delete User | Generate Token | Get All Books | Get Book |
| Get All Books | None | Get Book | Add Book to Collection → Get User |
| Get Book | None | Add Book to Collection | Replace Book → Get User |
| Add Book to Collection | Generate Token | Replace Book | Delete Book → Get User |
| Delete All Books | Add Book to Collection | Delete Book | Delete All Books → Get User |
| Delete Book | Add Book to Collection | Delete All Books | Delete User → Get User |
| Replace Book | Add Book to Collection | Delete User | |

**Note:** columns 3 (Order/Request) and 4 (Execution Flow) each represent independent top-to-bottom
sequences and are not row-aligned with columns 1–2.

## 8. Risks & Assumptions

- **Shared public demo environment:** Test data may be visible to, or collide with, other users of the same public API instance. No isolated/private test environment is available.
- **No guaranteed uptime or data persistence:** As a third-party demo service, availability and data retention are outside project control.
- **Documentation accuracy:** Swagger documentation is assumed accurate unless contradicted by actual observed API behaviour; any discrepancy found during execution is documented as a finding rather than silently worked around.
- **No access to server-side logs or source code:** All conclusions are based on observed request/response behaviour only (true black-box testing).

## 9. Test Deliverables

- Postman collection and environment (`postman/`)
- Structured test case suite (`test-cases/`)
- Execution/coverage summary (`execution/`)
- Defect reports (`defects/`)
- Supporting evidence — screenshots of key requests, responses, and findings (`evidence/`)
