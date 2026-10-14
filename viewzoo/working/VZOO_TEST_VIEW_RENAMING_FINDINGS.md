# Test View Renaming: Decision Record

## Problem

ViewZoo's test cases don't include `ALTER VIEW x RENAME TO y` variations. View renaming is a standard DDL operation that could regress undetected without coverage.

## Finding: rename was never supported

`ViewZooMetadata` did not override `renameView`, so Trino's SPI default rejected every `ALTER VIEW ... RENAME TO` with `NOT_SUPPORTED`, and the storage interface had no rename operation. A test-only item could only have asserted that failure, so the item was rescoped to implement rename and test it.

## Chosen approach: implement rename, then cover it

| Aspect | Detail |
|---|---|
| Metadata | `renameView` validates the target name with the same rules as `createView`, rejects a missing source or an existing target, then updates storage before the in-memory cache so a storage failure leaves the cache unchanged |
| JDBC storage | One `UPDATE` of the `(schema, view_name)` key — atomic |
| Filesystem storage | `Files.move` with `ATOMIC_MOVE`; source and target share one directory, so the move is a same-filesystem rename |
| Definition | Unchanged by rename — the stored catalog/schema is the resolution context for unqualified names, not the view's own name |
| Tests | One integration test per catalog: in-schema rename, cross-schema rename, existing target, missing source, invalid target name, persistence across restart |

## Alternatives considered

- **Broader DDL test sweep** — cover all missing DDL operations at once. Rejected: scope creep for a single-issue fix; other DDL gaps can be separate work items.
- **Assert rename is unsupported** — keep the test-only scope. Rejected: locks in a gap rather than closing it.
- **Split into a separate rename-support item** — Rejected: the tests are meaningless without the implementation.

## What this doesn't solve

- Test coverage for other DDL operations beyond rename
- Pre-existing ordering in `createView`, which updates the cache before storage