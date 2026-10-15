Implemented `DELETE /api/todos/{id}` in `lit-go-todos`:

- Successful deletion returns **204 with no body**; a missing ID returns **404**.
- Added SQLite store deletion and tests for list removal and absence after reopening the store.
- Updated API documentation in `README.md`.
- Left the frontend unchanged; no delete UI was added.

Checks passed: `make test`, `make build`, and `git diff --check`.
