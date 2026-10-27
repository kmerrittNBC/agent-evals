# Disposable qualification repository

This tiny repository is the frozen read/edit smoke fixture for gate 2. Copy
this directory into a new temporary directory and initialize Git there for
each attempt. Never run a candidate against this source template. The task is
to read `status.txt`, append `verified` on a new line, and report the diff.
The initial file must contain exactly `ready` followed by a newline.

The copied repository is disposable. Record its initial commit SHA and the
resulting diff in the run evidence. Use the same copied commit and prompt for
candidate and controls.
