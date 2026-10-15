Implemented completion filtering for `GET /api/todos` in `lit-go-todos`.

- `?completed=true` and `?completed=false` filter results without changing stored todos.
- Requests without the filter retain the existing ID ordering.
- Invalid, duplicate, empty, or malformed `completed` values return 400.
- Added focused Go tests for filtering, order, unchanged todo state, and invalid values; documented the query parameter in `README.md`.
- Left the Lit frontend and other endpoints unchanged.

I couldn’t run `make test` or `make build`: this environment provides no shell or command-execution tool.
