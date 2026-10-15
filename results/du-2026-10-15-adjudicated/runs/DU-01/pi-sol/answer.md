Added `DELETE /api/todos/{id}` in `main.go`. It removes the SQLite row, returns `204` with no body on success, and returns `404` when the ID is missing. Invalid IDs still receive `400`.

Updated `main_test.go` to cover deletion, repeat deletion, list results, and absence after reopening the store. Updated the API documentation in `README.md`. No delete UI was added.

`make test`, `make build`, and `git diff --check` passed. `npm ci` reported five high-severity dependency audit findings.
