# BookHub API — Test Closure / Summary Report

**Project:** BookHub API Quality Assurance
**Environment:** Public demo environment (`https://bookstore.toolsqa.com`)
**Tooling:** Postman, Swagger UI (reference)

## Testing Scope

Account & Authentication, Book Catalogue, User Collection Management, User Lifecycle, Negative & Error
Handling — as defined in `test-plan/Test-Plan.md` (Section 2). Basic credential-handling checks within
documented endpoints were included as part of standard contract validation.

## Out of Scope

Performance/load testing, active security/penetration testing, UI-layer testing.

## Execution Summary

| Metric | Count |
|---|---|
| Test cases planned | 27 |
| Test cases executed | 27 |
| Passed | 26 |
| Failed | 1 |
| Blocked | 0 |
| Defects raised | 1 |

## Defects

| Defect ID | Title | Priority | Status |
|---|---|---|---|
| DEF-001 | JWT payload exposes plaintext password | High | Open — Not Actionable (Third-Party API, No Dev Access) |

Full detail in [`defects/Bug-Tracker.md`](../defects/Bug-Tracker.md).

## Confirmed Business Rules

Open questions from test design, resolved through execution — not defects, included here for traceability.

| Behaviour Tested | Result |
|---|---|
| Adding a duplicate ISBN to a user's collection | Rejected — 400, error code `1210` |
| Replacing a book not in the user's collection | Rejected — 400, error code `1206` |
| Deleting a book not in the user's collection | Rejected — 400 |

## Exit Criteria — Met?

| Exit Criterion (from Test Plan, Section 6) | Status |
|---|---|
| All planned test cases executed and results recorded | Met — 27/27 executed, results recorded |
| All identified defects logged, with priority assigned and justified | Met — DEF-001 logged |
| High-severity defects re-verified against current live behaviour | Met, with documented exception — formal fix-and-retest not applicable (third-party API, no dev access); re-verified against live behaviour instead |
| Final execution/coverage summary produced | Met — this report |
| Known limitations and untested areas explicitly documented | Met — see below |

## Known Limitations

- **Boundary Conditions** were listed as in-scope in the Test Plan, but Swagger documentation defines no
  explicit field-length or range constraints for any endpoint in this API. No boundary test cases were
  executed, as inventing an arbitrary constraint not backed by a documented requirement would misrepresent
  it as a real limit.
- Performance/load testing and active security/penetration testing were out of scope and not performed.
- Testing was conducted against a shared public demo environment; test data may not persist and could be
  affected by concurrent use from other users of the same instance.

## Overall Conclusion

The BookHub API was tested end-to-end across account management, authentication, book catalogue, and
collection operations, covering positive, negative, business-rule, and data-handling scenarios. 27 of 27
planned test cases were executed, with 26 passing and one confirmed defect (DEF-001). All Exit Criteria
defined in the Test Plan were met, with one documented exception around defect retesting that reflects
the constraints of testing a third-party public API rather than a gap in process.
