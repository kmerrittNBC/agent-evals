Implemented `DELETE /api/todos/{id}` in `./lit-go-todos`. Successful deletes return **204 with no body**; missing IDs return **404**. The SQLite store removes the row, and tests verify it stays absent from the list and after reopening the store. Existing validation behavior is preserved, and no delete UI was added.

Updated `README.md` and replaced the test that expected DELETE to be unsupported. Added deletion coverage in `delete_test.go`; the evaluator-provided `eval_delete_test.go` was left unchanged.

**Checks passed:** `make test`, `make build`, and `git diff --check`.
