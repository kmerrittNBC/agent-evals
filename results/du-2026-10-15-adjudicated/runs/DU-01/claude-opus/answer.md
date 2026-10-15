`DELETE /api/todos/{id}` now works. A successful delete returns 204 with an empty body, and a missing ID returns 404. `make test` (Go and frontend tests) and `make build` both pass, and `go vet` is clean.

**`main.go`**
- **Store:** a new `Store.Delete(id)` runs a SQL delete and returns the existing "todo not found" error when no row was removed. The schema is unchanged.
- **Route:** the new route checks the ID the same way GET and PUT do, so a non-numeric or zero ID gets 400. A database failure returns 500.
- Create, read, update and validation code is unchanged.

**`main_test.go`**
- The old lifecycle test checked that DELETE returned 405. I renamed it `TestTodoLifecycle`; it now deletes the todo, then confirms the list is empty and GET returns 404.
- Added tests that:
  - deleting one todo leaves the others in the list;
  - deleting the same todo twice returns 404 the second time;
  - DELETE returns 404 for a missing ID and 400 for `abc` and `0`;
  - a deleted todo is still absent after the SQLite store is closed and reopened, while the remaining todo is still there.
- A small `performDelete` helper also checks that 204 responses have no body.

**`README.md`**
- Added the DELETE row to the API table, replaced the "deleting is intentionally not implemented" note with a line saying delete is API-only, and updated the description of what the tests cover.

**Not changed**
- **Frontend:** no delete UI and no change to `api.js`. The existing frontend test that checks there is no "Delete" control still passes.
- **`eval_delete_test.go`:** this untracked file was already in the worktree before I started. I left it alone; it runs and passes as part of the Go tests. `gofmt` reports it as unformatted (it uses spaces instead of tabs), but that's the only formatting issue.

The changes are not committed.
