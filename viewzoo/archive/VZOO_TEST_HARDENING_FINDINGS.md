# Test Hardening: Decision Record

## Problem

A one-off JaCoCo run on 2026-10-20, after PR #32 merged, measured 92% of lines and 93% of branches across the unit tests, the integration tests' JVM, and the plugin running inside the Trino container. No main path is untested, but these are:

- **Filesystem error paths** — `renameView` failing to link or to delete the source, `requireNoConflictingFile` failing to list the directory, and `createView` failing to delete its temp file.
- **Configuration checks** — an unreadable or unwritable `viewzoo.dir` (only a missing one is tested) and an invalid `viewzoo.storage_type`.
- **JDBC** — `renameView` failing for any reason other than a unique violation.
- **Uncalled methods** — Trino 483 and the tests never call `listTables`, `listViews`, `getColumnHandles`, `getColumnMetadata`, `getTableHandle`, `getTableMetadata`, `getTableProperties` or `ViewZooConnector.shutdown`.

One gap hides a bug. When `renameView` links the target but then fails to delete the source, it throws, so the cache keeps the old name while storage holds both files, and both views appear after a restart. That breaks the all-or-nothing rule storage-first ordering depends on.

## Preferred approach: fix the rename rollback, inject the failures permissions can't reach

| Aspect | Detail |
|---|---|
| Rename rollback | When the source delete fails, delete the new link before throwing, so storage is left as it was, but only while the target is still the same file as the source |
| Source already gone | A failed delete that removed the source anyway has completed the rename, so it is logged and reported as success, keeping the cache in step with storage (Rob) |
| Reachable by permissions | Rename link failure (read-only directory), listing failure (execute-only directory, where `Files.exists` works but `Files.list` doesn't), unreadable and unwritable directory |
| Needs a seam | Source delete and temp delete after a link, since both need the same directory write permission the link just used |
| Seam | An overridable delete in `ViewZooLocalFileSystemClient`, overridden by a failing test subclass, as `TestViewZooJdbcClient` overrides `getConnection` |
| Uncalled methods | Unit-test every one, so each has a pinned result (Rob) |

- **Fix, not just test** — a test of the failed delete has to assert something; asserting the duplicate would pin the bug (Rob).
- **Permissions first** — they exercise the real filesystem calls, and the seam is kept to the two cases they can't reach.
- **Existing precedent** — a test subclass overriding one method already isolates JDBC resource tracking.

## Alternatives considered

- **Test only, file the rename bug separately** — rejected by Rob: the new test would assert broken behavior or stay skipped.
- **Immutable files (`chflags uchg`)** — would make delete fail without a seam, but also blocks `link(2)` on macOS and needs root to undo on Linux.
- **A fault-injecting `FileSystem`** — the client uses the default filesystem through `File` and `dir.toPath()`, so this means re-plumbing the client for tests.
- **Leave the uncalled methods untested** — keeps tests to behavior Trino uses, but Rob chose pinned coverage.

## What this doesn't solve

- `createView`'s serialization failure and `isLoadable`'s null-name branch for filesystem names stay untested, since neither can happen.
- A crash between link and delete still leaves both files; only a failed delete rolls back.
- If the rollback delete also fails, both files remain, as after a crash.
- The check that the target is still the source's link and the rollback delete aren't atomic, so another writer replacing the target in between can still lose its view.
- Coverage is measured once, not gated in the build.
- Permission-based tests skip themselves when run as root.

## Reversals

None expected. The rename-by-hard-link finding in `VZOO_FINDINGS.md` says a crash between link and delete leaves a duplicate view; that stays true, and closeout should add that a failed delete now rolls back.
