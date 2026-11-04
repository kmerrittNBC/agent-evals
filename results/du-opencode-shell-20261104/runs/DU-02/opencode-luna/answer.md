Implemented optional `completed=true` and `completed=false` filtering for `GET /api/todos`. Requests without the filter retain the existing ID ordering; invalid or repeated values return 400. Filtering only affects the response, not stored todos or other endpoints.

Updated API documentation in `README.md` and added focused backend coverage in `api_filter_test.go`. Left the untracked `eval_filter_test.go` untouched.

Checks passed: `make test`, `make build`, and `git diff --check`.
