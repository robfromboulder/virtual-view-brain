# Storage Errors: Implementation Plan

## Objective

Make storage failures survivable and diagnosable. Loading views skips and logs any single entry that can't be read or parsed instead of failing the catalog, in both storage clients, and every wrapped storage exception keeps its cause and message. Targets the `v483` branch. Replaces GitHub issues #24 and #25. No new configuration, no change to the storage formats.

## Context

See `VZOO_STORAGE_ERRORS_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions (filesystem name rules and skip-on-load; storage-first ordering)
- `VZOO_APPROACH.md` — design constraints

## What changes

- `storage/ViewZooLocalFileSystemClient.java`
  - `getViews`: an entry that fails to read or parse (invalid or truncated JSON, a directory named `a.b.json`) is logged with its path and the exception, then skipped. Directory-level checks (missing, unreadable, unwritable) still fail the catalog.
  - `getViews`, `createView`, `dropView`: pass `e` as the cause and append `e.getMessage()`, matching `renameView`.
  - `renameView`: when the link target collides with a file stored under a different name (case-insensitive filesystem, e.g. a skipped `Collide.T.json`), report the same "View conflicts with an existing view file in filesystem storage" message as `createView`, not "View already exists".
- `storage/ViewZooJdbcClient.java`
  - `getViews`: a row whose `definition` fails to parse is logged with its schema and view name, then skipped. A failure of the query itself still fails the catalog.
  - Constructor, `getViews`, `createView`, `dropView`: pass `e` as the cause; add the missing ": " to the constructor message.
- `README.md` — extend the startup skip sentence to cover view files and rows that can't be read or parsed, in both storage types.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooMetadata` constructor calls `getViews` | Gets a partial map instead of an exception | A skipped view is invisible in SQL until fixed; only the log reveals it |
| Skip-on-load for unloadable file names (PR #27) | Same policy, extended to unreadable contents | Two warning messages should read as one family |
| `TestViewZooJdbcClient.testClosesResourcesOnParseFailure` | Parse failure no longer throws | Rewrite to assert the skip and that resources still close |
| `VZOO_PG_REFRESH` work item | Its live reload calls `getViews` | A bad row written live is skipped rather than breaking the reload; whichever merges second rebases |
| `VZOO_SAFE_CREATE` work item | Both edit the catch blocks of `createView` | Small rebase for whichever merges second |

## Testing approach

Unit (`mvn test`), in `TestViewZooLocalFileSystemClient`: an invalid JSON file, an empty (truncated) file and a directory named `a.b.json` are each skipped while a valid view beside them loads; a failed `dropView` (e.g. a non-empty directory named `s.t.json`) carries its cause and message; rename onto a case-colliding file reports the conflict message (case-insensitive host only, or covered in integration).

Integration (`-Pintegration`): in `TestViewZooJdbcClient`, a hand-inserted row with a bad definition is skipped and the other rows load. In `TestViewZooIntegration`, extend the skipped-file test: write a corrupt `schema.table.json` into `testfs` and `testfsmount`, restart, assert the warning in the log and that every other view still lists and queries.

The full unit and integration suites must stay green.

## Implementation sequence

1. Exception causes and messages in both clients (mechanical).
2. Skip-and-log in both `getViews`, with unit tests.
3. Rename collision message.
4. Integration tests and README.

## Scope boundary — what this does NOT include

- Atomic file writes and storage-level refusal on create (`VZOO_SAFE_CREATE`).
- Validating that a parsed definition's SQL still works; Trino reports that when the view is queried.
- Surfacing skipped entries anywhere but the log (a system table, a metric, a startup flag to fail instead).
- Retrying or repairing bad entries.

## Open issues

1. Confirm the logged exception message doesn't echo the definition text (Jackson's source-in-location setting), so a log line can't leak or flood with a large definition.
2. Whether a duplicate entry (e.g. two rows or files that resolve to the same `SchemaTableName`) also needs a defined skip rule.
