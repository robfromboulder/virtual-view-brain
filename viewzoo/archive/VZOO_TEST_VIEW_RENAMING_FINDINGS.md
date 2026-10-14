# Test View Renaming: Decision Record

## Problem

ViewZoo's test cases don't include `ALTER VIEW x RENAME TO y` variations. View renaming is a standard DDL operation that could regress undetected without coverage.

## Finding: rename was never supported

`ViewZooMetadata` did not override `renameView`, so Trino's SPI default rejected every `ALTER VIEW ... RENAME TO` with `NOT_SUPPORTED`, and the storage interface had no rename operation. A test-only item could only have asserted that failure, so the item was rescoped to implement rename and test it.

## Chosen approach: implement rename, then cover it

| Aspect | Detail |
|---|---|
| Metadata | `renameView` validates the target name with the same rules as `createView`, rejects a missing source or an existing target, then updates storage before the in-memory cache so a storage failure leaves the cache unchanged |
| JDBC storage | One `UPDATE` of the `(schema, view_name)` key — atomic; zero rows updated is `ViewNotFoundException`, a unique-key violation is `ALREADY_EXISTS` |
| Filesystem storage | Hard link to the target, then delete the source. `Files.move` without `ATOMIC_MOVE` only checks for the target before `rename(2)`, which still replaces it, so a racing writer loses its view; `link(2)` refuses an existing target atomically. A crash between link and delete leaves a duplicate, not a lost view. A missing source file is `ViewNotFoundException`, matching JDBC |
| Stale cache | The cache loads once at startup, so another coordinator or an external edit can make it disagree with storage. Both storage clients enforce source-exists and target-absent themselves rather than trusting the cache check, and when storage reports the source missing, `renameView` evicts it from the cache |
| Definition | Unchanged by rename — the stored catalog/schema is the resolution context for unqualified names, not the view's own name |
| Tests | One integration test per catalog: in-schema rename, cross-schema rename, existing target, missing source, invalid target name, persistence across restart. Trino's engine rejects existing-target and missing-source before calling the connector, so `TestViewZooMetadata` (with a fake storage client) covers the connector's own checks and `TestViewZooLocalFileSystemClient` covers the no-overwrite move |

## Alternatives considered

- **Broader DDL test sweep** — cover all missing DDL operations at once. Rejected: scope creep for a single-issue fix; other DDL gaps can be separate work items.
- **Assert rename is unsupported** — keep the test-only scope. Rejected: locks in a gap rather than closing it.
- **Split into a separate rename-support item** — Rejected: the tests are meaningless without the implementation.

## What this doesn't solve

- Test coverage for other DDL operations beyond rename
- Bugs found in review and filed instead of fixed here: path characters in view names (viewzoo#17), statement leaks in the JDBC client's older methods (viewzoo#19), `createView` and `dropView` updating the cache before storage (viewzoo#20). Filesystem rename after external file deletion (viewzoo#18) was filed, then fixed here after a second review