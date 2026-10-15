Implemented optional completion filtering for `GET /api/todos`. `completed=true` and `completed=false` return matching todos in ID order; omitting the parameter retains the existing full-list ordering. Invalid, empty, or repeated `completed` parameters return 400. No stored todos or other endpoints were changed.

Updated `main_test.go` to cover both filters, ordering, unfiltered results, and invalid values. Documented the query parameter and behavior in `README.md`.

**Checks:** `make test` and `make build` passed after installing frontend dependencies with `make install`. `npm ci` reported 5 high-severity dependency advisories.
