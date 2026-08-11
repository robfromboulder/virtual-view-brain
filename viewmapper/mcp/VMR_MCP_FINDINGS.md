# ViewMapper MCP Server: Implementation Findings

> V3, 2026-08-10.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## The session key is a constant, and the code looks like it isn't

Session identity is obtained through a function that always returns the same value. The indirection is deliberate: it marks the seam where a real session identifier would arrive if the protocol ever carried one, so the fix is a change inside one function rather than a hunt through the module. Read literally, the code appears to support multiple sessions and does not.

## The Python floor comes from the SDK, not from the code

The module requires a Python version well ahead of what most environments default to, and nothing in its own source needs it. The constraint is inherited from the MCP SDK. This matters only for local development, since the shipped container carries its own interpreter, and it is the reason a developer's system Python is usually the wrong one to run tests with.

## Startup cost was measured, not estimated

Launching the analysis subprocess costs three to five seconds before any work begins. Measured end to end, a simple question returns in five to ten seconds and a complex one on the largest available dataset in twenty to forty, so that startup is a large share of a fast answer and a rounding error on a slow one. Those figures are what make the fresh-process-per-question choice defensible rather than merely convenient, and they are the numbers to re-take before anyone argues for keeping a process warm.
