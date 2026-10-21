# FS Refresh: Decision Record

## Problem

Filesystem storage loads every view once at startup and never looks again, so a view file added, changed or deleted outside the connector stays invisible until Trino restarts (#14). The user who filed #14 runs this in production: Trino deployed with the official Helm chart, and view files synced from git by a Kubernetes cron job. Version-controlled view files are the reason the filesystem backend exists, so a restart per sync undercuts its main use.

## Preferred approach: timer-driven full reload

On a configurable interval, reload every view from storage and swap the in-memory map under the existing lock. Unset by default, so nothing changes for anyone who doesn't opt in.

| Aspect | Detail |
|---|---|
| Trigger | Fixed interval, off by default |
| Reload | Full `getViews()` and map swap, the same path as startup |
| Bad files | Skipped and logged, as at startup |
| Storage modes | Filesystem; JDBC open (see PLAN) |

- **Fits the sync pattern** — a cron job writes files and the next tick picks them up, with no coordination between the two.
- **Simplicity** — a full reload of a small directory reuses startup's code path and needs no change tracking.
- **Opt-in** — the in-memory, load-once behavior stays the default.

## Alternatives considered

- **Fall through to storage on a cache miss** (proposed in #14) — finds new views but never changed or dropped ones.
- **Directory watching** — immediate, but `WatchService` is unreliable on network and container-mounted volumes, which is where synced directories live.
- **A scalar function to refresh** (discussed in #14) — a function with a side effect is the wrong Trino construct; a procedure is the right shape, and whether to add one is open.

## What this doesn't solve

- Views are stale for up to one interval after a sync.
- A sync that writes files non-atomically can be read halfway, losing or reverting a view for one interval.
- Every coordinator reloads on its own schedule, so coordinators can briefly disagree.

## Reversals

- `VZOO_APPROACH.md`, Key Design Decisions — "Everything is cached in memory, loaded once at startup, and never watched." Becomes false for filesystem storage when refresh is configured.
- `VZOO_SCOPE.md`, Open Questions — "Whether the store must tolerate its contents changing from outside the engine." Answered yes for filesystem storage.
