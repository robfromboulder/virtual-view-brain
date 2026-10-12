# PG Refresh: Implementation Plan

## Objective

Make JDBC storage refresh views live across coordinators. A Postgres trigger on the `viewzoo` table sends a notification on every change, and each coordinator listens and reloads its in-memory views. Targets the `v483` branch. No new infrastructure, no change to the table's columns, no change to filesystem mode's behavior.

## Context

See `VZOO_PG_REFRESH_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `storage/ViewZooStorageClient.java` — add a way for a client to report that storage changed, e.g. registering a callback. Default is a no-op, so the filesystem client needs no change.
- `storage/ViewZooJdbcClient.java` — at startup, create the notify function and a statement-level `AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE` trigger beside the existing `CREATE TABLE IF NOT EXISTS`. Open a dedicated connection, run `LISTEN viewzoo`, and start a daemon thread that polls `PGConnection.getNotifications(timeout)`, fires the callback once per non-empty batch, and reconnects with backoff on failure, firing the callback after each reconnect.
- `ViewZooMetadata.java` — register the callback, and on callback reload `storageClient.getViews()` and swap the map inside the existing lock.
- `src/test/docker/trino/catalog/` — add a PostgreSQL connector catalog over the same database, so tests can write to the table directly.
- `TestViewZooIntegration.java` — add the refresh tests (see Testing approach).
- `README.md` — change the startup-refresh limitation so it applies to filesystem storage only, and say that JDBC storage refreshes live, including after direct writes to the table. Note the extra privileges the JDBC user needs.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooMetadata` map and `synchronized` methods | Reload swaps the map under the same lock | A reload during DDL must not lose the write; the lock serializes them |
| `createView` updates the cache before storage | Unchanged here | A failed write fires no trigger, so the phantom view persists until the next change to the table triggers a reload; that fix is a separate item |
| `ViewZooJdbcClient` startup DDL | Gains function and trigger creation | Extra privileges are needed; `CREATE OR REPLACE TRIGGER` needs Postgres 14+ |
| `VZOO_WHY_VIEWZOO` work item | Adds the startup-refresh limitation and possibly the PG connector test catalog this item edits | Whichever merges second rebases onto the other |
| One `DriverManager` connection per operation | The listener adds one long-lived connection per coordinator | Holds one slot in the connection limit |

## Testing approach

Integration tests in `TestViewZooIntegration` against the existing docker-compose stack, using the new PG connector catalog to write rows directly:

- An out-of-band insert (copying a view's row under a new name) becomes visible through `testjdbc` within a bounded wait.
- An out-of-band delete removes the view from `testjdbc` within the same bound.
- An out-of-band update to a definition changes the view's query result.

The existing `testjdbc`/`testfs` data-provider suite must stay green. Testing two coordinators needs a second Trino container. That check lives in `VZOO_PG_REFRESH_TESTING.md` unless it proves cheap to automate.

## Implementation sequence

1. Storage-change callback on the interface; metadata reload and swap.
2. Trigger and notify function DDL in the JDBC client.
3. Listener thread with drain, coalesce and reconnect.
4. PG connector test catalog and integration tests.
5. README refresh statement.

## Scope boundary — what this does NOT include

- README positioning: "Why ViewZoo?", the two modes as workflows, pairing with the PG connector (`VZOO_WHY_VIEWZOO`).
- Refresh for filesystem storage (timer, reload function, or fall-through on cache miss); #14 stays open for it.
- The small JDBC fixes: duplicate schema names from `listSchemaNames`, cache updated before the storage write, the missing ": " in the startup error.
- A connection pool, configurable schema or table name, `jsonb` definitions, metadata columns, a history table, multi-tenancy (#10), security-mode enforcement (#13).

## Open issues

1. Minimum supported Postgres version: the README promises 10 or higher, but `CREATE OR REPLACE TRIGGER` needs 14+. Either raise the stated minimum or drop and recreate the trigger to keep 10.
2. What happens when the JDBC user can't create the trigger: fail startup, or log a warning and run without refresh.
3. Listener poll timeout and reconnect backoff values.
4. Whether the two-coordinator check is worth automating with a second Trino service in docker-compose.
