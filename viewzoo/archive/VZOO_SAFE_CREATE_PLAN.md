# Safe Create: Implementation Plan

## Objective

Make `createView` all-or-nothing in storage and make storage, not the cache, refuse a create without `OR REPLACE` when the view already exists. Filesystem storage writes a temp file and then hard-links it into place for a new view or atomically moves it for a replace; JDBC storage uses a plain `INSERT` for a new view and keeps the upsert for a replace. Targets the `v483` branch. Replaces GitHub issues #28 and #29. No new configuration, no change to the storage formats.

## Context

See `VZOO_SAFE_CREATE_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions (rename by hard link; storage-first ordering; trusting storage over the cache)
- `VZOO_APPROACH.md` — design constraints

## What changes

- `storage/ViewZooStorageClient.java` — `createView` takes `boolean replace`.
- `ViewZooMetadata.java` — pass `replace` through. Keep the cache check as a fast path; storage is now the authority.
- `storage/ViewZooLocalFileSystemClient.java` — `createView`:
  1. Validate the name and run the case-collision check (`requireNoConflictingFile`) before writing anything.
  2. Write the definition to a temp file in the view directory named `.viewzoo-<uuid>.tmp`: hidden and not ending in `.json`, so `getViews` never loads it, and a fixed 49 bytes, so it fits the 255-byte limit for any view name.
  3. Without `replace`: `Files.createLink(path, temp)`; `FileAlreadyExistsException` becomes `ALREADY_EXISTS`. With `replace`: `Files.move(temp, path, ATOMIC_MOVE)`.
  4. Delete the temp file in `finally`.
- `storage/ViewZooJdbcClient.java` — `createView`: without `replace`, a plain `INSERT`, mapping `UNIQUE_VIOLATION` to `ALREADY_EXISTS` as `renameView` does; with `replace`, the existing upsert.
- `TestViewZooMetadata.FakeStorageClient` — accept `replace` and refuse an existing view without it.
- `README.md` — if it states filesystem requirements, add that creating a view needs hard links, as renaming already does.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `renameView` hard-link pattern | Create reuses it | Create now also fails on filesystems without hard links |
| `requireNoConflictingFile` collision check | Must run before the link or move | Running it after would let a case-colliding replace overwrite another view's file |
| `getViews` file filter (`!isHidden && endsWith(".json")`) | Must ignore temp files | A temp name ending in `.json` would load as a view after a crash |
| Cache check in `ViewZooMetadata.createView` | Stays as a fast path | Storage refusing a view the cache lacks leaves the cache stale until restart; refresh is #14 / `VZOO_PG_REFRESH` |
| `UNIQUE_VIOLATION` mapping in JDBC `renameView` | JDBC create reuses it | — |

## Testing approach

Unit (`mvn test`), in `TestViewZooLocalFileSystemClient`: create without `replace` onto an existing file fails with `ALREADY_EXISTS` and leaves the file unchanged; create with `replace` swaps the contents; no temp file remains after success or failure; a leftover temp file isn't loaded by `getViews`. In `TestViewZooMetadata`: `replace` reaches storage, and storage refusing a view absent from the cache surfaces `ALREADY_EXISTS` without changing the cache.

Integration (`-Pintegration`): in `TestViewZooJdbcClient`, create without `replace` onto an existing row fails with `ALREADY_EXISTS` and leaves the definition unchanged, and `testCreateReplacesView` passes with `replace`. In `TestViewZooIntegration`, against every catalog: write a view into storage behind the connector's back (a file into `testfs`/`testfsmount`, a row into PostgreSQL), then `CREATE VIEW` of the same name fails with `ALREADY_EXISTS` and the stored definition survives.

A failed write partway (full disk) is hard to automate; cover it by asserting the target is untouched when the temp write throws, using a fake or a read-only temp, or move it to `VZOO_SAFE_CREATE_TESTING.md`.

## Implementation sequence

1. Interface, metadata and fake storage client.
2. JDBC `createView`.
3. Filesystem temp-then-link/move, with unit tests.
4. Integration tests and README.

## Scope boundary — what this does NOT include

- Skip-and-log on load and exception causes (`VZOO_STORAGE_ERRORS`).
- Atomic `dropView`, or making rename's link-then-delete crash-safe.
- Refreshing the cache from storage (#14, `VZOO_PG_REFRESH`).
- A fallback for filesystems without hard links.
- `fsync` of the file or directory for durability across power loss.

## Resolved questions

1. Temp files left by a crash are ignored, not deleted on load: load never modifies storage, and deleting could remove another coordinator's in-flight temp file (Rob).
2. Temp files are named `.viewzoo-<uuid>.tmp`, unique across coordinators and independent of the view name's length (Rob).
3. A create with `replace` accepts the race where a different-case file appears between the collision check and the move, as create already does (Rob).
