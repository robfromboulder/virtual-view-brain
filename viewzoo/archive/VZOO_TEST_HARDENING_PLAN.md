# Test Hardening: Implementation Plan

## Objective

Cover the code paths the 2026-10-20 JaCoCo run found untested, and fix the rename bug one of them hides: a failed source delete after a successful link leaves both files in storage. Failures are induced with filesystem permissions where possible, and through one overridable delete method where permissions can't isolate them. Targets the `v483` branch. No new configuration, no change to the storage formats.

## Context

See `VZOO_TEST_HARDENING_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_FINDINGS.md` — rename by hard link; storage-first ordering requires all-or-nothing writes; safe create
- `VZOO_APPROACH.md` — design constraints

## What changes

- `storage/ViewZooLocalFileSystemClient.java`:
  - `renameView`: when deleting the source fails, delete the target link, then throw `GENERIC_INTERNAL_ERROR` with the original cause.
  - Route the source delete and the temp-file delete through one overridable method, so a test subclass can make it fail.
- `TestViewZooLocalFileSystemClient`:
  - rename into a read-only directory fails with "Failed to link file" and leaves the source
  - rename whose source delete fails throws, leaves the source, and leaves no target
  - create whose temp delete fails still succeeds and writes the view
  - create or rename onto an existing file in an execute-only directory fails with "Failed to list directory"
  - an unreadable or unwritable directory fails load with `CONFIGURATION_INVALID`
- New `TestViewZooStorageClientProvider`: an invalid `viewzoo.storage_type` fails with `CONFIGURATION_INVALID`.
- `TestViewZooJdbcClient`: rename after the table is dropped keeps its `SQLException` cause, alongside the existing create and drop checks.
- `TestViewZooMetadata`: `listTables` and `listViews` with and without a schema, the table-handle methods returning null, and `getTableProperties`.
- A test for `ViewZooConnector.shutdown`.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| Rename by hard link | Rollback added after a failed delete | A rollback that deletes the wrong path would lose the view; the target is a fresh link to the source, so deleting it loses nothing |
| `deleteTempFile` logs instead of throwing | Its failure becomes testable through the seam | — |
| Permission-based tests | Same pattern as `testReplaceDoesNotWriteInPlace` | Skip as root; must restore permissions in `finally` so `tearDown` can delete the directory |

## Testing approach

All new tests are unit tests (`mvn test`) except the JDBC rename failure, which joins `TestViewZooJdbcClient` under `-Pintegration`. The full unit and integration suites must stay green. After the work, rerun the coverage measurement in `VZOO_TEST_HARDENING_CLAUDE.md` to confirm each listed gap is covered.

## Implementation sequence

1. Failing test for the rename rollback, then the fix.
2. The seam, and the temp-delete test through it.
3. Permission-based filesystem tests.
4. Provider, JDBC and metadata tests.
5. Connector shutdown test.
6. Coverage rerun.

## Scope boundary — what this does NOT include

- Making rename crash-safe between link and delete.
- A coverage gate in the build, or keeping JaCoCo in the pom.
- Changing what the uncalled methods return.
- The metadata test's fake storage modelling real rename refusals (existing target, missing source, `failWrites`).

## Resolved questions

1. The seam is a package-private `deleteFile(Path)` in `ViewZooLocalFileSystemClient`, used for the source delete and the temp delete, and overridden by an anonymous test subclass.
2. When the rollback delete also fails, the original failure is thrown with the rollback's exception attached as suppressed, and both files remain.
3. `ViewZooConnector` is built through `ViewZooConnectorFactory` with Trino's `TestingConnectorContext`, which `trino-main` already supplies as a test dependency.
