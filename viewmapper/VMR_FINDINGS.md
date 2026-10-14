# ViewMapper: Implementation Findings

> V2, 2026-10-13.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## The server's deadline has to cover several model calls, not one

One question can make several model calls in sequence, each bounded by the analysis program's own per-call timeout, so the conversational side's deadline must exceed a multiple of that timeout rather than the timeout itself. Raising the output-token cap to 16000 in ViewMapper PR #10 pushed a single call past 60 seconds, so the per-call timeout went to 180 seconds. The server's deadline went first to 300 seconds, and a review showed that two calls near their limit already exceed it, so it went to 600. Anyone changing either number has to change the other with it.
