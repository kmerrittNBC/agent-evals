Updated `GET /api/todos` to accept only `completed=true` or `completed=false`. Without the parameter, it retains the existing list and ID ordering. Invalid, empty, or repeated values return HTTP 400. Filtering only reads stored todos; other endpoints are unchanged.

Added focused Go tests and updated `README.md`. After installing frontend dependencies, `make test`, `make build`, and `git diff --check` passed. The pre-existing untracked `eval_filter_test.go` was left untouched.
