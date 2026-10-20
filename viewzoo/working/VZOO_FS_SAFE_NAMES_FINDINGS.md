# FS Safe Names: Decision Record

## Problem

Filesystem storage builds each view's path by `dir.resolve(schema + "." + table + ".json")` from names Trino passes through unchanged from quoted identifiers, and only `.` and overlong names are rejected. On Trino 483 (Linux container) and macOS, measured end to end:

- `/` in a name fails the write with `GENERIC_INTERNAL_ERROR`, or, if the subdirectory exists, writes a file `getViews` never reloads (#17).
- A schema starting with `/` resolves as absolute and writes outside `viewzoo.dir` wherever the Trino user can write.
- NUL throws an unchecked `InvalidPathException` instead of a `TrinoException`.
- A filename over 255 UTF-8 bytes fails on Linux but succeeds on macOS, so a view directory written on a Mac can hold files a Linux server cannot create — a real hazard for directories shared through git.
- Renaming to a name containing `/` fails in `link(2)` with `NoSuchFileException`, which the client reports as the source view missing; the metadata layer then evicts a source that is still on disk, and it vanishes until restart.

Everything else tried round-trips on both platforms and through restart: spaces, `\ : * ? < > | " ' %`, tab, newline, leading/trailing spaces, accented, CJK and emoji names.

## Preferred approach: reject unrepresentable names inside the filesystem client

The filesystem client rejects a name it cannot store as one flat file, before touching the disk, and its path builder refuses any resolved path that is not a direct child of the views directory.

| Aspect | Detail |
|---|---|
| Rejected | `/` or NUL in schema or table; `schema.table.json` over 255 UTF-8 bytes |
| Where | `createView` and the `renameView` target, plus a containment check in `viewPath` |
| Error | `INVALID_ARGUMENTS`, matching the existing name rules |
| JDBC | Unaffected |

- **Backward compatible** — `/` and NUL never produced a loadable view on the filesystem, so no stored view becomes unreachable; the only names newly refused that once worked are over-255-byte names on macOS.
- **Right layer** — the restriction belongs to the storage that has it; JDBC stores and reloads `/` correctly.
- **Defense in depth** — the containment check holds even if a later name rule is wrong.
- **Portable directories** — the 255-byte limit is enforced on macOS too, so a directory valid on a Mac is valid on Linux.

## Alternatives considered

- **Blocklist in `ViewZooMetadata.validateName` (PR #21, closed)** — applied a filesystem limit to JDBC, breaking names JDBC handles, and rejected `\`, which works on both platforms; left `viewPath` unchecked.
- **Escape unsafe characters in filenames** — would let any name be stored, but changes the on-disk format, makes files harder to read and review, and needs migration for existing directories.
- **Containment check alone** — closes the escape, but `/` within a name would still fail late with an internal error, and NUL and overlong names would still fail with unclear errors.

## What this doesn't solve

- Windows hosts.
- Names that differ only in Unicode normalization collide on APFS but not on Linux.
- Case-insensitive filesystems are not an issue only because Trino lowercases names before the connector sees them.
