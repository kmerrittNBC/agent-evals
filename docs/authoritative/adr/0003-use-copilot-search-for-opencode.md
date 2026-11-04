---
status: accepted
supersedes: 0002-readmit-opencode-arm
---

# Use Copilot-backed web search for OpenCode

The original OpenCode arm used TinyFish while Pi used provider-native web
search through the authenticated GitHub Copilot model. This made the two Luna
arms differ on search as well as on the coding agent. OpenCode V2 supports
registered web-search providers. The pinned `opencode-websearch@0.7.1` plugin
registers its `native` provider and uses OpenCode's active Copilot connection
with the Responses API `web_search` tool. A live probe on OpenCode 2.0.26
observed completed `websearch` and `webfetch` calls with real Python
documentation results. The runner sets the default model to the same Copilot
Luna model used for the agent; the plugin selects its default model for search.

Pin the plugin version and `native` provider in the arm definition and in the
per-process OpenCode configuration. Keep the existing deny-by-default tool
permissions and standalone server. Static preflight rejects any other search
route; live preflight requires completed search and fetch calls. These searches
consume Copilot model usage, which must be included in future credit analysis.

The original IG attempts also revealed a separate workspace error. Python's
`subprocess.Popen(cwd=...)` changed the child working directory but left the
inherited `PWD` environment variable pointing at the evaluator checkout.
OpenCode used that value to locate the project. In a Linux A/B probe, a
relative `read` missed a marker file with the stale `PWD` and read it
successfully when `PWD` matched the disposable workspace. The runner now sets
`PWD` for OpenCode, checks a real `read` result during live preflight, and
runs its IG attempts in a Bubblewrap view that hides judge evidence and the
configured source checkouts. The pinned exported repository trees remain visible.

The new IG run is a fresh attempt with two changed conditions: search route
and workspace visibility. Its outcome cannot isolate the effect of search
quality. Keep the October IG artifacts and prior reports as historical
observations.
