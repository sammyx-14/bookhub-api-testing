# BookHub API Quality Assurance

Black-box testing of the BookHub (Book Store) REST API at `https://bookstore.toolsqa.com`, run first in Postman and then automated in Python with a CI pipeline.

**Result:** 30 test cases, 29 passed and 1 failed. The failure confirms one defect (DEF-001): the token returned by Generate Token carries the user's password in plain text. The automated suite has 37 tests and runs in GitHub Actions.

The Test Plan, Test Cases, Defect Report and Test Summary Report are on the project page: [BookHub API Quality Assurance](https://damilareakanni.framer.website/projects/bookhub-api-quality-assurance). This repository holds the code and the run evidence.

## Repository structure

```
bookhub-api-testing/
├── postman/
│   ├── BookStore API.postman_collection.json
│   └── BookStore - Dev.postman_environment.json
├── evidence/
│   └── screenshots/          Postman run, DEF-001 token, Allure report and CI run
├── automation/
│   ├── api/                  API client for the Account and BookStore operations
│   ├── tests/                account, bookstore and e2e tests
│   ├── TRACEABILITY.md       test case ID mapped to its automated test
│   ├── make_traceability.py  generates TRACEABILITY.md from the test code
│   └── requirements.txt
└── .github/workflows/tests.yml
```

## Run the Postman collection

1. Import both files from `postman/` into Postman.
2. Select the **BookStore - Dev** environment. `baseUrl` is already set to `https://bookstore.toolsqa.com`.
3. Run the collection with the Collection Runner, from the first request, in the order it is saved. Later requests depend on the user the first ones create.

Credentials are generated at run time by a collection-level pre-request script, so no setup is needed beyond the steps above. The collection deletes the users it creates at the end.

Keep the environment variables as the default type. If `token` is stored as a secret, Postman does not send it, and every request that needs a Bearer token returns 401.

Expected result: 44 requests and 76 assertions, 75 passed and 1 failed. The failure is TC-007, which confirms DEF-001.

## Run the automated suite

From the `automation` folder, with Python 3.14, the version the pipeline uses:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

`pytest` runs the tests in their written order. To run them in random order, as the pipeline does, use `pytest -p randomly`. Each test creates its own user and deletes it afterwards, so the order makes no difference.

To open the Allure report (needs Node.js):

```
npx allure generate reports/allure-results -o reports/allure-report
npx allure open reports/allure-report
```

Expected result: 37 tests collected, 36 passed and 1 expected failure. TC-007 is marked as an expected failure linked to DEF-001. The mark is strict, so the test fails if the API ever stops exposing the password.

## Traceability

[`automation/TRACEABILITY.md`](automation/TRACEABILITY.md) maps every test case ID to the pytest function and file that checks it. To regenerate it after changing the tests, run `python make_traceability.py` from the `automation` folder.

## Continuous integration

GitHub Actions runs the suite on every push to the `main` branch, in random order, and publishes the Allure report as a downloadable artifact. See the **Actions** tab.

## Credentials

No API keys, tokens or personal credentials are stored in this repository. Test users are generated at run time and deleted at the end of each run.
