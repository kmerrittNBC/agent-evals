`GET /api/todos` now accepts an optional `completed=true` or `completed=false` filter, and any other value gets a 400. `make test` and `make build` both pass, and `go vet` is clean.

**Behaviour**
- **No `completed` parameter:** returns every todo ordered by id, exactly as before.
- **`completed=true` / `completed=false`:** returns only the matching todos, still ordered by id. If nothing matches you get `[]`, not `null`.
- **Anything else:** returns 400 with `{"error":"completed must be \"true\" or \"false\""}`. This includes an empty value (`completed=`), different case (`TRUE`), `1` or `0`, and the parameter appearing twice. I chose this strict rule on purpose rather than Go's lenient boolean parsing, since the task says to reject any other value.

**Changes**
- **`main.go`:** `Store.List` now takes an optional filter. When it's empty, the database query is the same as before. A new `readCompletedFilter` function checks the query parameter, and the GET handler uses it. There's no schema change, and the other endpoints are untouched.
- **`main_test.go`:** three new tests:
  - Unfiltered, completed and incomplete results, with the order checked using interleaved completed and incomplete todos.
  - A filter with no matches returns `[]`.
  - Each invalid value above returns 400 with an error message, and the stored todos are unchanged afterwards.
- **`README.md`:** documents the `completed` parameter in the API section and updates the "Current behavior" and "Verify" sections, as AGENTS.md requires.
- **Frontend:** no changes. The UI still loads the unfiltered list, so the existing frontend tests (2 passing) cover it.

**Things to know**
- The worktree already had an untracked `eval_filter_test.go` that I didn't write. I left it alone and it passes. It isn't gofmt-formatted (it uses spaces for indentation).
- AGENTS.md mentions a Gitea issue; I didn't look it up, since you said this prompt is the task record.
- Running the checks needed `make install` (`npm ci`), because the frontend dependencies weren't installed. npm reported some audit warnings, which I didn't investigate.
- Nothing is committed.
