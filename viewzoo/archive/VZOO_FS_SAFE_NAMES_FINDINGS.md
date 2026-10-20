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

The filesystem client rejects a name it cannot store as one flat file, before touching the disk, and its path builder refuses any resolved path that is not a direct child of the views directory. It asks the filesystem, rather than predicting it, whether a new view would land in another view's file.

| Aspect | Detail |
|---|---|
| Rejected | `/` or NUL in schema or table; names not in NFC; `schema.table.json` over 255 UTF-8 bytes |
| Where | `createView` and the `renameView` target, plus a containment check in `viewPath` |
| Collisions | `createView` refuses with `ALREADY_EXISTS` when the file exists but the directory listing lacks that exact name; rename relies on `link(2)` refusing an existing target |
| Loading | Files whose names aren't lowercase NFC `schema.table.json` are skipped with a logged warning |
| Error | `INVALID_ARGUMENTS`, matching the existing name rules |
| JDBC | Unaffected |

- **Mostly backward compatible** — `/` and NUL never produced a loadable view. Newly refused or skipped: over-255-byte names on macOS, non-NFC names, and files with uppercase names, which loaded before but whose drop and replace missed the file on Linux.
- **Right layer** — the restriction belongs to the storage that has it; JDBC stores and reloads `/` correctly.
- **Defense in depth** — the containment check holds even if a later name rule is wrong.
- **Portable directories** — the 255-byte limit is enforced on macOS too, so a directory valid on a Mac is valid on Linux.

## Alternatives considered

- **Blocklist in `ViewZooMetadata.validateName` (PR #21, closed)** — applied a filesystem limit to JDBC, breaking names JDBC handles, and rejected `\`, which works on both platforms; left `viewPath` unchecked.
- **Escape unsafe characters in filenames** — would let any name be stored, but changes the on-disk format, makes files harder to read and review, and needs migration for existing directories.
- **Containment check alone** — closes the escape, but `/` within a name would still fail late with an internal error, and NUL and overlong names would still fail with unclear errors.
- **Case-fold rule in Java (tried, reverted)** — rejected names changed by per-character case mapping; missed APFS's one-to-many folds (`ß`/`ss`, `ﬀ`/`ff`) and made Greek names ending in capital sigma uncreatable.
- **`toRealPath` for the collision check (tried, reverted)** — returns the stored name on macOS but the requested name on Linux, so it misses collisions on case-insensitive Linux mounts.
- **Failing startup on unloadable file names** — rejected by Rob in favour of skipping with a warning, so one stray file can't take down the catalog.

## What this doesn't solve

- Windows hosts.
- HFS+ stores names as NFD and limits them to 255 UTF-16 units, so a valid name of many multiply-accented characters could fail there with an internal error; accepted as a known issue.
- Another process creating a colliding file between the collision check and the write.
- On a Linux host the integration tests have no case-insensitive directory, so that path is measured only when tests run on macOS.
