# Storage Errors: Implementation Plan

## Objective

Make storage failures survivable and diagnosable. Loading views skips and logs any single entry that can't be read, parsed or keyed instead of failing the catalog, in both storage clients, and every wrapped storage exception keeps its cause and message. Targets the `v483` branch. Replaces GitHub issues #24 and #25. No new configuration, no change to the storage formats.

## Context

See `VZOO_STORAGE_ERRORS_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions (filesystem name rules and skip-on-load; storage-first ordering)
- `VZOO_APPROACH.md` — design constraints

## What changes

- `storage/ViewZooLocalFileSystemClient.java`
  - `getViews`: a file whose read or parse throws `IOException` (invalid, empty or truncated JSON, a directory named `a.b.json`) or whose parse returns null (the JSON literal `null`) is skipped with the warning `Skipping file whose contents are not a view definition: <path>: <e.getMessage()>`, omitting the trailing `: <message>` for a null result. Directory-level checks (missing, unreadable, unwritable) still fail the catalog.
  - `getViews`, `createView`, `dropView`: pass `e` as the cause and append `e.getMessage()`, matching `renameView`.
  - `renameView`: before linking, run the same check as `createView`: when the target exists but `isExactFile(target)` is false (a case-insensitive filesystem resolved it to a file stored under a different name, e.g. a skipped `Collide.T.json`), throw `ALREADY_EXISTS` with "View conflicts with an existing view file in filesystem storage". An exact existing target still reaches the link, whose atomic refusal keeps "View already exists". The check runs before the link because `isExactFile` throws `IOException`, which a catch clause of the same `try` can't handle.
- `storage/ViewZooJdbcClient.java`
  - `getViews`: each row is handled on its own.
    - A row whose `schema` or `view_name` is empty or not lowercase (`name.equals(name.toLowerCase(ENGLISH))`) is skipped with `Skipping row whose name is not a view name Trino can create: <schema>.<view_name>`.
    - A row whose `definition` is SQL NULL, fails to parse, or parses to null is skipped with `Skipping row whose definition is not a view definition: <schema>.<view_name>: <e.getMessage()>`, omitting the trailing `: <message>` when there is no exception.
    - A `SQLException` from the query, `next()` or `getString` still fails the catalog, so the per-row catch must not cover it.
  - Constructor, `getViews`, `createView`, `dropView`: pass `e` as the cause; add the missing ": " to the constructor message.
- `README.md` — extend the startup skip sentence: filesystem storage also skips any file whose contents aren't a view definition, and JDBC storage skips any row whose schema or view name is empty or not lowercase, or whose definition isn't a view definition.

Warnings log `e.getMessage()`, not the exception, so a log line carries no stack trace per bad entry. Jackson 2.22 redacts the source from its messages and truncates echoed tokens, so the message can't leak or flood with a large definition (measured: a 100 KB invalid token gives a 468-character message).

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooMetadata` constructor calls `getViews` | Gets a partial map instead of an exception | A skipped view is invisible in SQL until fixed; only the log reveals it |
| `ViewZooMetadata.getViews` copies the map with `ImmutableMap.copyOf` | Relies on no null value ever entering the map | A null definition fails every listing of the catalog, which is why a null parse result is skipped |
| Skip-on-load for unloadable file names (PR #27) | Same policy, extended to contents and to JDBC rows | The new warnings follow its `Skipping <entry> whose …` wording |
| `TestViewZooJdbcClient.testClosesResourcesOnParseFailure` | Parse failure no longer throws | Rewrite to assert the skip and that resources still close |
| `TestViewZooLocalFileSystemClient.testCaseInsensitiveCollisionRejected` | Rename collision message changes | Assert the conflict message, not only the error code |
| `TestViewZooIntegration.testFileNameCollision` | Asserts `"already exists"` for the case-insensitive rename | Change to `"conflicts with an existing view file"` |
| `VZOO_PG_REFRESH` work item | Its live reload calls `getViews` | A bad row written live is skipped rather than breaking the reload; whichever merges second rebases |
| `VZOO_SAFE_CREATE` work item | Both edit the catch blocks of `createView` | Small rebase for whichever merges second |

## Testing approach

Unit (`mvn test`), in `TestViewZooLocalFileSystemClient`:
- Invalid JSON, an empty file, truncated JSON, `{}`, the literal `null` and a directory named `a.b.json` are each skipped while a valid view beside them loads.
- A failed `dropView` (a non-empty directory named `s.t.json`) and a failed `createView` (a directory named `s.t.json`) carry the cause and its message.
- `testCaseInsensitiveCollisionRejected` asserts the conflict message for the rename; it already skips itself on a case-sensitive filesystem.
- A missing directory still fails the load with `CONFIGURATION_INVALID`, guarding against a catch that is too broad.

Integration (`-Pintegration`):
- `TestViewZooJdbcClient`: hand-inserted rows with a definition of `'not json'`, SQL NULL and `'null'`, an empty schema, an empty view name, and an uppercase name beside a lowercase row of the same name are each skipped while the valid rows load; the parse-failure resources test asserts the skip and that every resource still closes; a `SQLException` from the query (drop the table first) still throws.
- `TestViewZooIntegration`:
  - `testUnreadableFileSkipped` writes `hidden.corrupt.json` (invalid JSON) or `hidden.nulldef.json` (`null`) into `testfs` and `testfsmount`, one restart per case, and asserts that `hidden.ok` queries, that `information_schema.views` lists only `ok`, and the warning in the log. It is a separate test from `testUnsupportedFileNamesSkipped` so a crash can't mask that test's assertions.
  - `testUnloadableRowsSkipped` inserts rows through `psql` into `testjdbc`'s table (a bad definition, a NULL definition, and an empty and an uppercase name copying a valid definition) and makes the same assertions with the JDBC warnings.
  - `testFileNameCollision` asserts the new rename message on a case-insensitive directory.
  - A bad entry stops the Trino server, so these tests clean up without relying on it: mounted files are deleted from the host, and `recoverTrino` recreates the container when Trino isn't ready, which discards files written inside it.

The full unit and integration suites must stay green.

## Implementation sequence

Test-first: no signature changes, so every test above compiles against the current code.

1. Write every new and changed test, with no change under `src/main`. Run `mvn test` and `mvn test -Pintegration` on a macOS host, and log which tests fail; that list is the measured exposure.
2. Exception causes and messages in both clients (mechanical).
3. Skip-and-log in both `getViews`, including null results and JDBC row names.
4. Rename collision message.
5. README. Every test from step 1 now passes, and the full suites stay green.

## Scope boundary — what this does NOT include

- Atomic file writes and storage-level refusal on create (`VZOO_SAFE_CREATE`).
- Validating that a parsed definition's SQL still works; Trino reports that when the view is queried.
- Surfacing skipped entries anywhere but the log (a system table, a metric, a startup flag to fail instead).
- Retrying or repairing bad entries.
- JDBC rows whose names Trino accepts but ViewZoo refuses to create (containing `.`, over 100 characters); they key correctly and drop and rename still match them.

## Open issues

None.
