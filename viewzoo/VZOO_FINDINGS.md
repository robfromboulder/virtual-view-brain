# ViewZoo: Implementation Findings

> V11, 2026-10-20.

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

The filesystem client renames by hard link, then deletes the source. `Files.move` with `ATOMIC_MOVE` silently replaces an existing target on POSIX, and without it the existence check precedes `rename(2)`, which still replaces a target written in between; `link(2)` refuses an existing target atomically. A crash between link and delete leaves a duplicate view, never a lost one. A failed delete rolls back instead (PR #33): the target is removed only while it is still the same file as the source, which narrows but can't close the window in which another writer replaces it. If the source is confirmed gone and the target confirmed present, the failed delete took effect anyway, so the rename is reported as completed, keeping the cache in step with storage (Rob). An unreadable state falls through to the rollback, since `Files.notExists` and `Files.exists` are each true only when confirmed. Filesystems without hard links, such as some network or FUSE mounts, cannot rename, and since PR #32 cannot create views either.

Because the engine pre-empts both conflict cases, SQL-level tests pass even with the connector's checks deleted; those checks are unit-tested against a fake storage client instead. Established by PR #16 (`a9eb9a5`, `adccc71`, `6e6304f`).

## 5. Closing keywords do not fire on version-branch PRs

GitHub acts on `Closes #N` only when a PR merges into the default branch. ViewZoo PRs target the current version branch, which is not the default (`v479` while `v483` is current), so issues a PR fixes must be closed by hand after the merge. Found when PR #16 merged into `v483` and left #18 open.

## 6. Storage-first ordering requires all-or-nothing storage writes

`createView`, `dropView` and `renameView` write storage first and update the cache only when storage succeeds (PR #23, `10abcc1`, fixing #20). That keeps cache and storage in agreement only if a failed storage write changes nothing. Filesystem `createView` originally broke this by writing the view's file in place (#28), and without `OR REPLACE` it checked only the cache while both clients overwrote (#29); PR #32 fixed both, as the safe create finding records.

The PR #23 review also raised that a JDBC connection close that throws after autocommit reports a committed write as failed, leaving the cache behind storage. It was not filed: closing a PostgreSQL connection rarely throws after a successful commit, and the old cache-first order failed in the mirror-image case.

## 7. Docker-dependent tests belong in the `integration` group

The default `mvn test` stays free of Docker, so any test that needs Docker joins the TestNG `integration` group, even a self-contained Testcontainers test that needs no built plugin. Skipping such a test when Docker is absent was rejected: under `-Pintegration` the Compose-based tests fail without Docker, so a skip would let a run pass with no JDBC coverage. The cost is that `TestViewZooJdbcClient` (PR #30) runs only under `-Pintegration`. Code reviews flag this as a coverage gap on every pass; it is a deliberate choice, not an oversight.

## 8. Filesystem name rules ask the filesystem rather than model it

Filesystem storage refuses names it can't store as one flat file, and the rules live in `ViewZooLocalFileSystemClient` because JDBC stores and reloads the same names correctly; a blocklist in `ViewZooMetadata.validateName` (PR #21, closed) broke working JDBC names. Measured through Trino on Linux and macOS, including a restart, only `/` and NUL are unstorable; `\ : * ? < > | " ' %`, control characters and non-ASCII all round-trip, so they stay accepted. Linux limits a file name to 255 bytes and macOS doesn't, so the limit is enforced on macOS too, keeping a directory shared through git loadable on both.

Case-insensitive filesystems fold names in ways Java can't reproduce. APFS maps `ß` to `ss` and `ﬀ` to `ff`, which a rule built from per-character case mapping misses, and that rule also made Greek names ending in capital sigma uncreatable. `toRealPath` returns the stored name on macOS but the requested name on a case-insensitive Linux mount, so it misses collisions there. Both were tried and reverted, so the collision check compares the exact directory listing; reviews keep proposing `toRealPath` as a cheaper check.

Java on macOS reports directory listings in NFC, so an NFD file loads there rather than being skipped, and no test of skipping NFD files can run on macOS. Files whose names Trino couldn't create are skipped with a warning rather than failing startup, so one stray file can't take the catalog down. The integration tests' only case-insensitive Linux directory is a macOS bind mount, because OrbStack's kernel lacks Unicode casefolding. HFS+, which stores names as NFD under a UTF-16 length limit, is an accepted untested gap. Established by PR #27 (`b1827b7`, `ca3dfcc`, `26dbb25`, `345916a`, `65e6897`), fixing #17.

## 9. Storage skips unreadable entries instead of failing load

A catalog whose connector fails to construct stops the whole Trino server at startup (exit 100, measured on Trino 483), so one view file or row that couldn't be read once took down every catalog on the server. Anyone able to write one bad entry, or one write that failed partway, could deny service to every view. Both storage clients therefore skip, with a one-line warning, any entry they can't read, parse or key, and still fail load when the directory, database or query itself fails, since no partial result would mean anything there. Rob set this as a fixed policy for both clients. Failing loudly, a flag choosing fail or skip, and quarantining or repairing the entry on load were rejected: the failing mode is never the safe one, and load must not modify storage. Logging the exception message can't leak or flood a definition, because Jackson 2.22 redacts its source and truncates echoed tokens.

Read errors are skipped like parse errors. Rob kept that after review proposed failing load on I/O errors, accepting the cost: a valid entry that is briefly unreadable at startup is skipped, and `CREATE OR REPLACE VIEW` of its name silently replaces it. A skipped entry stays in storage but is invisible to Trino: `DROP VIEW` reports it missing, while a plain `CREATE VIEW` or a rename onto its name reports it exists (plain create since PR #32), and removing it means editing storage directly.

JDBC skips rows whose schema or view name is empty or not lowercase. Trino lowercases every name ViewZoo stores, so only a row written outside Trino can be affected, and such a row was already broken before the change: it loaded under its lowercased name, which drop, rename and replace all missed. Each client's `parse` reports a NULL or JSON-null definition by throwing, so the warning carries a reason; reviews flag this as exceptions for control flow. Established by PR #31 (`7259591`, `265ba77`, `42357f9`), fixing #24 and #25.

## 10. Create writes a whole file and lets storage refuse an existing view

Two fixes had to land together. Writing a temp file and moving it into place with `ATOMIC_MOVE` makes a write all-or-nothing, but `rename(2)` silently replaces an existing target, which a plain `CREATE VIEW` must refuse. So filesystem create writes `.viewzoo-<uuid>.tmp` and hard-links it into place for a new view, since `link(2)` refuses an existing target atomically, and moves it atomically only for `OR REPLACE`. Rejected: `ATOMIC_MOVE` for every create (replaces), `CREATE_NEW` (writes in place), an existence check before the move (not atomic), and falling back to non-atomic writes without hard links (silent behavior differences; deferred). JDBC uses a plain `INSERT` for a new view and keeps the upsert for a replace.

Rob decided that leftover temp files are ignored rather than deleted on load, since load never modifies storage and deleting could remove another coordinator's in-flight file. Rob also chose a fixed-length UUID name, independent of the view name's length, and accepted the race where a different-case file appears between the collision check and a replace's move, as create already accepts. A failed temp delete is logged rather than thrown, because throwing after the link would report a completed create as failed.

Accepted costs: a replace swaps in a new file, dropping a mode or owner set by hand and turning a symlinked view file into a regular one, since keeping either means writing in place; without `fsync` a power loss can still lose a completed write; and when storage refuses a view the cache lacks, the cache stays stale until restart. Established by PR #32 (`7e862cb`, `0054a25`), fixing #28 and #29.

## 11. Storage error paths are forced with permissions, and one seam

A 2026-10-20 coverage run, including the plugin inside the Trino container, found every main path covered and the error paths not. Directory permissions force most failures through the real filesystem calls: a read-only directory fails a link or a write, an execute-only one resolves a path but can't be listed, and the tests skip themselves when run as a user who ignores permissions. A delete that follows a link needs the same directory permission the link just used, so permissions can't fail it alone; those deletes go through a package-private `deleteFile` that a test subclass overrides. Immutable files and a fault-injecting `FileSystem` were rejected, the first for blocking links on macOS and needing root on Linux, the second for re-plumbing the client.

Rob chose to unit-test the SPI methods no integration test reaches, so their not-found results are pinned. Coverage after the work was 98.9% of lines and 97.8% of branches; the rest can't happen: a serialization failure, an `InvalidPathException` after names are validated, and a null name at the filesystem's name check. Reviews flag concurrent-writer races around the rename rollback on every pass; they are accepted, as other races are. Established by PR #33 (`af881e0`, `531df42`, `3990c82`).

## 12. Releases are built on the maintainer's Mac, not by a workflow

Rob didn't want the build and test environment published as a GitHub Actions workflow, so releases follow the procedure in the repository's `CLAUDE.md`, run by Claude on Rob's Mac. A committed release script was rejected for the same reason. A macOS build matches a Linux one because the plugin is pure Java with no native code. A draft release has no tag until it's published, so a draft can be checked without using up a letter. Also rejected: Maven Central, since Trino plugins are installed by copying a directory and publishing there needs signing keys; bare-version tags, since a fix would then replace an archive someone already downloaded; a release on every push, since that publishes unreviewed states; and a Trino image with ViewZoo installed, a second artifact that could follow later.

Rob decided that older version branches get no binaries, that releases attach no sources because the tag marks them, and that release notes carry no checksum, since GitHub shows each asset's SHA-256 and the README doesn't check one. A binary's provenance is therefore only its tag and the maintainer's machine: no recorded build run exists, and binaries carry no signature or attestation. The README picks the newest release with a matching version prefix rather than following `releases/latest`, because every version branch shares one release list. Established by PR #34 (`a9a7b60`, `cbffa36`, `cced25d`, `837fc9a`), fixing #12.
