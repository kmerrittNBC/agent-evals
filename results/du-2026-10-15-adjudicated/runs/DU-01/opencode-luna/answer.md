Implemented `DELETE /api/todos/{id}` in `./lit-go-todos`. Successful deletes return `204` with no body; missing IDs return `404`. Deleted todos are removed from SQLite, and tests cover their absence from the list and after reopening the store. Existing create, read, update, and validation behavior was left unchanged.

Updated `README.md` with the endpoint behavior and added backend regression coverage. **No delete UI was added**; the existing frontend test checks that there is no delete control.

I couldn’t run `make test` or `make build` because this session provides no command-execution tool. Those checks remain to be run locally.
