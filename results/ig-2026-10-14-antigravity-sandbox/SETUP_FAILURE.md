# Antigravity sandbox permission attempt

This supplementary attempt is excluded from quality comparison. The first
preflight was launched without the local certificate environment and failed
TLS verification. A corrected preflight passed. During all five task runs,
Antigravity CLI requested the `command` permission and headless mode denied it
because no explicit allow rule was configured. The first attempted repository
command in IG-03 was `ls -la`; the event trace records the automatic denial.

The main evaluation remains
`results/ig-2026-10-14-five-arm-v2`. A separate follow-up evaluation with
`command(*)` explicitly allowed inside `--sandbox` is
`ig-2026-10-14-antigravity-command-allowed`.
