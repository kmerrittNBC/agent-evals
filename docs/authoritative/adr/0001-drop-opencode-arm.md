---
status: accepted
---

# Drop the OpenCode evaluation arm

The OpenCode arm was included to measure an open-source harness using the Copilot-backed `gpt-6-luna` model, as part of a fallback plan for a scenario where the business provides no additional AI tooling support. OpenCode requires a separate web-search provider for the evaluation's search-and-fetch capability check; that provider needs its own organization approval, account or key, and billing, unlike the existing Copilot-supported setup. Keeping the arm would therefore make the fallback depend on precisely the additional tooling support it is meant to work without, while duplicating the model already evaluated through Pi and adding setup time against the Monday completion target. Drop the OpenCode arm and evaluate the remaining supported arms without substituting a model or search provider. The evaluation therefore has five arms and 25 run slots. Reconsider OpenCode if its required search capability becomes available through the existing Copilot support without additional organizational spend.
