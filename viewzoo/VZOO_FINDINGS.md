# ViewZoo: Implementation Findings

> V2, 2026-08-10.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## 1. READ_COMMITTED is the only declared isolation level

The connector reports READ_COMMITTED because that is the least restrictive level Trino accepts, and nothing about the store's behavior would differ under a stricter one. View operations are synchronized and served from an in-memory map, so there is no concurrent-read anomaly to prevent and no write ordering beyond the lock. Declaring a stricter level would promise semantics the store does not implement; READ_COMMITTED matches what actually happens.
