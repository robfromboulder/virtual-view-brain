# FS Safe Names: Implementation Plan

## Objective

Make filesystem storage refuse, with a clear `INVALID_ARGUMENTS` error, any view name it cannot store as one flat `schema.table.json` file on Linux or macOS, instead of failing with an internal error, writing a file it never reloads, writing outside `viewzoo.dir`, or losing a view on a failed rename. The protections live in the filesystem storage client only, so JDBC storage keeps accepting every name it accepts today. Tests describing the desired behavior land first, failing against unmodified `v483`, and the protections follow on the same branch. No change to JDBC storage, the metadata layer, or the on-disk format.

## Context

See `VZOO_FS_SAFE_NAMES_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `ViewZooLocalFileSystemClient` — `createView` and the `renameView` target reject a schema or table name containing `/` or NUL, and a filename (`schema.table.json`) longer than 255 UTF-8 bytes, with `INVALID_ARGUMENTS`. `viewPath` additionally verifies the resolved path is a direct child of `viewzoo.dir` with the expected filename, so no future name rule can let a path escape.
- `TestViewZooLocalFileSystemClient` — desired-behavior tests: portable names round-trip; `/`, absolute names, an existing subdirectory, NUL, and overlong filenames are rejected with no file written anywhere; renaming to a rejected name leaves the source intact; a filename of exactly 255 bytes is accepted.
- `TestViewZooIntegration` — portable names round-trip on both catalogs and survive restart; storage-specific limits per catalog (JDBC unchanged, filesystem rejections carry the new error); a failed filesystem rename leaves the source queryable without a restart.
- `README.md` — one line in the filesystem storage section naming what it rejects.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooMetadata.validateName` (rejects `.` and names over 100 chars, all storage types) | Unchanged; runs before the filesystem checks | None |
| `ViewZooMetadata.renameView` evicts the source when storage reports it missing | The target is now rejected before `link(2)`, so a missing target directory can no longer be misreported as a missing source | None |
| PR #23 (storage before cache in `createView`/`dropView`) | Independent; tests here do not assert cache state after a failed write | Low — trial merge clean |
| `getViews` loading existing files | Names loaded from disk can't contain `/` or NUL, so drop and rename-source never see them | None |

## Testing approach

Unit tests in `TestViewZooLocalFileSystemClient` against a temp directory with views one level below a test-owned root, so an escaping path stays inside test space and is observable. Integration tests in `TestViewZooIntegration` run on Linux (the Trino container), which is where the 255-byte filename limit is real. The first commit adds only tests; its failures are the specification. Full unit and integration suites must be green after the second commit.

## Implementation sequence

1. Commit desired-behavior tests; confirm which fail on unmodified `v483`.
2. Commit the filesystem client protections and README line; confirm all suites green.
3. Open draft PR against `v483` referencing #17.

## Scope boundary — what this does NOT include

- Windows. Trino servers run on Linux (macOS for development); drive letters and Windows-reserved characters are not handled.
- Any change to JDBC storage or to which names it accepts.
- Rejecting `\`, `:`, `*?<>|"`, control characters other than NUL, or non-ASCII — all round-trip on Linux and macOS today and stay accepted.
- Cache ordering on failed writes (PR #23).
- Unicode normalization differences between macOS and Linux.

## Open issues

1. Whether to reject names that differ only in Unicode normalization (NFC vs NFD), which APFS maps to one file and Linux to two.
