# ViewMapper MCP Server: Implementation Findings

> V2, 2026-08-02.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## The session key is a constant, and the code looks like it isn't

Session identity is obtained through a function that always returns the same value. The indirection is deliberate: it marks the seam where a real session identifier would arrive if the protocol ever carried one, so the fix is a change inside one function rather than a hunt through the module. Read literally, the code appears to support multiple sessions and does not.

## The Python floor comes from the SDK, not from the code

The module requires a Python version well ahead of what most environments default to, and nothing in its own source needs it. The constraint is inherited from the MCP SDK. This matters only for local development, since the shipped container carries its own interpreter, and it is the reason a developer's system Python is usually the wrong one to run tests with.

## Startup cost was measured, not estimated

Launching the analysis subprocess costs several seconds before any work begins, which is a meaningful share of a fast question and a rounding error on a slow one. That measurement is what makes the fresh-process-per-question choice defensible rather than merely convenient, and it is the number to re-take before anyone argues for keeping a process warm.
