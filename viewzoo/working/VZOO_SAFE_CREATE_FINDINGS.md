# Safe Create: Decision Record

## Problem

Two defects in `createView` break the rule that a storage write either succeeds completely or changes nothing, which storage-first ordering depends on.

- **Writes in place (#28).** Filesystem `createView` uses `Files.writeString`, which empties the file first. A write that fails partway, e.g. on a full disk, leaves a truncated `schema.table.json`, for a new view or a replaced one; the old definition is lost and, until `VZOO_STORAGE_ERRORS` lands, the catalog won't load on restart.
- **Checks only the cache (#29).** Without `OR REPLACE`, `ViewZooMetadata.createView` checks the in-memory cache, then both clients overwrite unconditionally: JDBC with `on conflict do update`, the filesystem with `writeString`. A view added to storage after the cache loaded — by another coordinator (#10) or an outside change (#14) — is silently replaced instead of failing with `ALREADY_EXISTS`.

The two must be fixed together: the obvious fix for #28, a temp file moved into place with `ATOMIC_MOVE`, silently replaces an existing target on POSIX, which is exactly what #29 forbids.

## Preferred approach: temp file, then link or move

Write the definition to a temp file in the same directory. Without `replace`, hard-link it to the view's path, since `link(2)` atomically refuses an existing target; with `replace`, `Files.move` it with `ATOMIC_MOVE`. Delete the temp file either way. JDBC gets the same split: plain `INSERT` without `replace`, the upsert with it.

| Aspect | Detail |
|---|---|
| Temp file | Same directory, hidden, not ending in `.json`, unique per write |
| New view | `Files.createLink`; existing target → `ALREADY_EXISTS` |
| Replace | `Files.move(..., ATOMIC_MOVE)` |
| Collision check | Before the link or move |
| JDBC | `INSERT`; `UNIQUE_VIOLATION` → `ALREADY_EXISTS` |

- **All-or-nothing** — the view's path only ever holds a complete old or complete new definition.
- **Storage is the authority** — an existing view is refused even when the cache doesn't know it.
- **Consistent with rename** — the same `link(2)` reasoning already chosen for `renameView`.

## Alternatives considered

- **Temp file plus `ATOMIC_MOVE` for every create** (as #28 proposed) — atomic, but replaces an existing target and so can't satisfy #29.
- **`Files.write` with `CREATE_NEW`** — refuses an existing file atomically, but writes in place, reintroducing #28 for new views.
- **Existence check, then move** — the check and the `rename(2)` aren't atomic, so a target written in between is replaced.
- **Fall back to non-atomic writes without hard links** — keeps those filesystems working at the cost of silent behavior differences; deferred.

## What this doesn't solve

- Filesystems without hard links, such as some network or FUSE mounts, now can't create views either.
- The cache still doesn't learn about a view that storage refused; it stays stale until restart.
- Without `fsync`, a power loss can still lose a completed write.

## Reversals

- `VZOO_FINDINGS.md`, the finding that storage-first ordering requires all-or-nothing writes: its claims that filesystem `createView` writes in place (#28) and that `createView` checks only the cache while both clients overwrite (#29) become false.
- `VZOO_FINDINGS.md`, the rename-by-hard-link finding: "Filesystems without hard links … cannot rename" extends to creating views.
