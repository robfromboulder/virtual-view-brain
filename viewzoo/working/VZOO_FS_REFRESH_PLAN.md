# FS Refresh: Implementation Plan

## Objective

Let filesystem storage pick up view files changed outside the connector, such as by a git sync job, without restarting Trino. A configurable timer reloads every view from storage and swaps the in-memory map; it is off by default. Targets the `v483` branch. Replaces GitHub issue #14. No change to the storage format.

## Context

See `VZOO_FS_REFRESH_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `config/` — a refresh interval property (name to settle, e.g. `viewzoo.refresh_interval`), as an Airlift `Duration`, unset meaning no refresh.
- `ViewZooMetadata.java` — reload `storageClient.getViews()` and swap the map inside the existing lock, as `VZOO_PG_REFRESH` also needs.
- A scheduled daemon executor that runs the reload on the interval, stopped when the connector shuts down.
- `README.md` — document the property, the staleness window it leaves, and the sync pattern it supports.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `synchronized` metadata methods | Reload swaps the map under the same lock | DDL during a reload must not be lost; reading storage before taking the lock keeps the lock short, but then a write in between must not be overwritten |
| `VZOO_STORAGE_ERRORS` work item (blocker) | Reload depends on skip-and-log | Without it, one half-synced file fails the reload |
| `VZOO_SAFE_CREATE` work item | Its temp files sit in the view directory | Reload must ignore them, as `getViews` will |
| `VZOO_PG_REFRESH` work item | Builds the same reload-and-swap | Whichever merges first builds it; the other rebases onto it |

## Testing approach

Unit: reload replaces, adds and removes views from a fake storage client; a DDL call racing a reload keeps its write. Integration: against `testfs` and `testfsmount` with a short interval, a file copied in becomes queryable, a deleted file disappears and an edited file changes the query result, each within a bounded wait. The existing suite stays green with refresh unset.

## Implementation sequence

1. Reload-and-swap in `ViewZooMetadata`, with unit tests (or rebase onto `VZOO_PG_REFRESH`'s).
2. Config property and scheduler.
3. Integration tests and README.

## Scope boundary — what this does NOT include

- JDBC refresh by notification (`VZOO_PG_REFRESH`).
- Watching the directory for changes (inotify, `WatchService`).
- Falling through to storage on a cache miss.
- Incremental reload of only the changed files.

## Open issues

1. Whether an on-demand refresh (a connector procedure such as `CALL <catalog>.system.refresh_views()`) is in scope alongside the timer, for a sync job to trigger right after it writes.
2. Whether the timer applies to JDBC storage too, as a fallback where the trigger can't be created.
3. When a file that loaded before fails to read on reload (e.g. mid-sync), whether to keep its previous definition or drop the view until the next reload.
4. The default and minimum interval, and whether reload logs a summary of what changed.
