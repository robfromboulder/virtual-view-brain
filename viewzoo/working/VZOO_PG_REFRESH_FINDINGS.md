# PG Refresh: Decision Record

## Problem

JDBC storage exists so that coordinators can share one durable store, but every coordinator loads its views once at startup and never looks again. Two coordinators or clusters sharing one Postgres table drift apart after the first write until restarted, and a row written straight into the table — by a GitOps sync job, say — is never seen at all. This is issue #14, and it bites JDBC mode harder than filesystem mode because sharing is the reason to choose JDBC.

## Preferred approach: trigger-driven LISTEN/NOTIFY with full reload

A statement-level trigger on the `viewzoo` table calls `pg_notify('viewzoo', '')` after any insert, update, delete or truncate. Each coordinator holds one dedicated connection that has run `LISTEN viewzoo`, polled by a background daemon thread. When any notification arrives, the connector reloads every view from the table and swaps the in-memory map under the existing lock. Filesystem mode is unchanged.

| Aspect | Detail |
|---|---|
| Notification source | Trigger on the table, created at startup alongside the table |
| Trigger granularity | `FOR EACH STATEMENT`, so a bulk sync costs one notification, not one per row |
| Delivery | Postgres delivers on commit, so a reload always reads committed rows |
| Reload | Full `getViews()` and map swap; notifications drained in one poll coalesce into one reload |
| Listener failure | Reconnect with backoff, then reload unconditionally, since notifications sent while disconnected are lost |
| Storage interface | Gains a way to signal "storage changed" upward; the filesystem client never signals |

- **Out-of-band writes** — the trigger fires however the row changed, so a sync job or a PG connector `INSERT` is seen exactly like a write from another coordinator. Notifying from the connector's own write path would miss both.
- **No timer** — changes arrive within moments with no polling interval to tune and no load while idle.
- **Simplicity** — a full reload of a small table avoids applying deltas, and a reload is already how the cache is built at startup.
- **No new infrastructure** — the same table and driver, plus one function and one trigger.

## Alternatives considered

- **Application-side `NOTIFY` after each connector write** — simpler DDL, but blind to direct writes to the table, which are half of the problem.
- **Timer-based reload** — works for both storage modes, but trades staleness against load and still leaves a window of drift. It remains the likely answer for filesystem mode (`VZOO_FS_REFRESH`).
- **Fall through to storage on cache miss** — proposed in #14. It finds views that are new, but not views that changed or were dropped.
- **Incremental update from the notification payload** — avoids a full reload, but a payload is capped at 8000 bytes and a delta protocol is more code than a small table justifies.
- **Reload function callable from SQL** — useful for filesystem sync, but an extra step every writer must remember. Out of scope here.

## What this doesn't solve

- Filesystem mode still loads once at startup; the `VZOO_FS_REFRESH` work item covers it.
- A coordinator serves stale views for the moment between a commit and its reload; there is no read-your-writes guarantee across coordinators.
- A reload replaces the whole map, so at some unmeasured store size it becomes the bottleneck.
- The JDBC user must be allowed to create a function and a trigger, which a locked-down database may refuse.

## Reversals

- `VZOO_APPROACH.md`, Key Design Decisions — "Everything is cached in memory, loaded once at startup, and never watched." Becomes false for JDBC storage, which now watches the table.
- `VZOO_SCOPE.md`, Open Questions — "Whether the store must tolerate its contents changing from outside the engine." Answered yes for JDBC storage, but still open for the filesystem.
