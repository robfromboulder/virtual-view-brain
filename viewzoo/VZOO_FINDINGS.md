# ViewZoo: Implementation Findings

> V8, 2026-10-20.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## 1. READ_COMMITTED is the only declared isolation level

The connector reports READ_COMMITTED because that is the least restrictive level Trino accepts, and nothing about the store's behavior would differ under a stricter one. View operations are synchronized and served from an in-memory map, so there is no concurrent-read anomaly to prevent and no write ordering beyond the lock. Declaring a stricter level would promise semantics the store does not implement; READ_COMMITTED matches what actually happens.

---

## 2. A Trino upgrade aligns runtime-supplied dependencies to Trino, not to their newest releases

Slice, `jackson-annotations` and OpenTelemetry are supplied by Trino at runtime, so the pom pins them to the versions the target Trino release ships (its Airbase), and Airlift to the version Trino itself uses. Only the PostgreSQL driver is bundled with the plugin, so it alone moves to its current release. Maven Central's search API lags new releases; confirm a dependency's current version from the repository's `maven-metadata.xml`. Established by the Trino 483 upgrade (PR #15, `2b3240a`).

Trino's plugin loader performs no SPI version check, so a build for one release can load into another; passing integration tests against a newer Trino image is how to tell whether an upgrade needs source changes or only version bumps. The 479 build passed all integration tests against Trino 483 unmodified.

## 3. `hero.svg` carries its text as outlined paths

The README hero image draws its text as glyph outlines, so a text search for a version number or date misses it; only `hero.src.svg` holds the text as `<text>`. A version sweep must search `hero.src.svg`. Re-rendering `hero.svg` from the source with Inkscape alters the artwork (rounded enclosure corners, lost SQL indentation), so until the original render tool is known, change its text by outlining only the affected strings and swapping those paths in at their existing positions. Established by the 483 badge fix (PR #15, `f376256`).

## 4. Rename trusts storage, not the cache, to detect conflicts

Trino's `RenameViewTask` rejects a rename onto an existing view, or of a missing one, before calling the connector, and `renameView` repeats both checks. Both read the in-memory cache, so neither catches a cache that disagrees with storage — another coordinator sharing the store, or a file changed outside Trino. Each storage client therefore enforces source-exists and target-absent itself, and when storage reports the source missing, `renameView` evicts the stale cache entry.

The filesystem client renames by hard link, then deletes the source. `Files.move` with `ATOMIC_MOVE` silently replaces an existing target on POSIX, and without it the existence check precedes `rename(2)`, which still replaces a target written in between; `link(2)` refuses an existing target atomically. A crash between link and delete leaves a duplicate view, never a lost one. Filesystems without hard links, such as some network or FUSE mounts, cannot rename.

Because the engine pre-empts both conflict cases, SQL-level tests pass even with the connector's checks deleted; those checks are unit-tested against a fake storage client instead. Established by PR #16 (`a9eb9a5`, `adccc71`, `6e6304f`).

## 5. Closing keywords do not fire on version-branch PRs

GitHub acts on `Closes #N` only when a PR merges into the default branch. ViewZoo PRs target the current version branch, which is not the default (`v479` while `v483` is current), so issues a PR fixes must be closed by hand after the merge. Found when PR #16 merged into `v483` and left #18 open.

## 6. Storage-first ordering requires all-or-nothing storage writes

`createView`, `dropView` and `renameView` write storage first and update the cache only when storage succeeds (PR #23, `10abcc1`, fixing #20). That keeps cache and storage in agreement only if a failed storage write changes nothing. Filesystem `createView` breaks this: `Files.writeString` empties the file before writing, so a failed write leaves a corrupt file, which load skips on restart, losing that view (#28). `createView` also doesn't follow §4's rule of trusting storage over the cache: without `OR REPLACE` it checks only the cache, and both storage clients overwrite (#29).

The PR #23 review also raised that a JDBC connection close that throws after autocommit reports a committed write as failed, leaving the cache behind storage. It was not filed: closing a PostgreSQL connection rarely throws after a successful commit, and the old cache-first order failed in the mirror-image case.

## 7. Docker-dependent tests belong in the `integration` group

The default `mvn test` stays free of Docker, so any test that needs Docker joins the TestNG `integration` group, even a self-contained Testcontainers test that needs no built plugin. Skipping such a test when Docker is absent was rejected: under `-Pintegration` the Compose-based tests fail without Docker, so a skip would let a run pass with no JDBC coverage. The cost is that `TestViewZooJdbcClient` (PR #30) runs only under `-Pintegration`. Code reviews flag this as a coverage gap on every pass; it is a deliberate choice, not an oversight.

## 8. Filesystem name rules ask the filesystem rather than model it

Filesystem storage refuses names it can't store as one flat file, and the rules live in `ViewZooLocalFileSystemClient` because JDBC stores and reloads the same names correctly; a blocklist in `ViewZooMetadata.validateName` (PR #21, closed) broke working JDBC names. Measured through Trino on Linux and macOS, including a restart, only `/` and NUL are unstorable; `\ : * ? < > | " ' %`, control characters and non-ASCII all round-trip, so they stay accepted. Linux limits a file name to 255 bytes and macOS doesn't, so the limit is enforced on macOS too, keeping a directory shared through git loadable on both.

Case-insensitive filesystems fold names in ways Java can't reproduce. APFS maps `ß` to `ss` and `ﬀ` to `ff`, which a rule built from per-character case mapping misses, and that rule also made Greek names ending in capital sigma uncreatable. `toRealPath` returns the stored name on macOS but the requested name on a case-insensitive Linux mount, so it misses collisions there. Both were tried and reverted, so the collision check compares the exact directory listing; reviews keep proposing `toRealPath` as a cheaper check.

Java on macOS reports directory listings in NFC, so an NFD file loads there rather than being skipped, and no test of skipping NFD files can run on macOS. Files whose names Trino couldn't create are skipped with a warning rather than failing startup, so one stray file can't take the catalog down. The integration tests' only case-insensitive Linux directory is a macOS bind mount, because OrbStack's kernel lacks Unicode casefolding. HFS+, which stores names as NFD under a UTF-16 length limit, is an accepted untested gap. Established by PR #27 (`b1827b7`, `ca3dfcc`, `26dbb25`, `345916a`, `65e6897`), fixing #17.

## 9. Storage skips unreadable entries instead of failing load

A catalog whose connector fails to construct stops the whole Trino server at startup (exit 100, measured on Trino 483), so one view file or row that couldn't be read once took down every catalog on the server. Anyone able to write one bad entry, or one write that failed partway, could deny service to every view. Both storage clients therefore skip, with a one-line warning, any entry they can't read, parse or key, and still fail load when the directory, database or query itself fails, since no partial result would mean anything there. Rob set this as a fixed policy for both clients. Failing loudly, a flag choosing fail or skip, and quarantining or repairing the entry on load were rejected: the failing mode is never the safe one, and load must not modify storage. Logging the exception message can't leak or flood a definition, because Jackson 2.22 redacts its source and truncates echoed tokens.

Read errors are skipped like parse errors. Rob kept that after review proposed failing load on I/O errors, accepting the cost: a valid entry that is briefly unreadable at startup is skipped, and until `createView` refuses to overwrite (#29) a plain `CREATE VIEW` of its name silently replaces it, in both storage types. A skipped entry stays in storage but is invisible to Trino: `DROP VIEW` reports it missing, a rename onto its name reports it exists, and removing it means editing storage directly.

JDBC skips rows whose schema or view name is empty or not lowercase. Trino lowercases every name ViewZoo stores, so only a row written outside Trino can be affected, and such a row was already broken before the change: it loaded under its lowercased name, which drop, rename and replace all missed. Each client's `parse` reports a NULL or JSON-null definition by throwing, so the warning carries a reason; reviews flag this as exceptions for control flow. Established by PR #31 (`7259591`, `265ba77`, `42357f9`), fixing #24 and #25.
