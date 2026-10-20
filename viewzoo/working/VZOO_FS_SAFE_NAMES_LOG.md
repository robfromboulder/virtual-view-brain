# FS Safe Names: Session Log

Running log of implementation sessions. Each session appends after a `---` separator.

The first entry, and every one after it, follows the entry format and content rules in `VV_SESSION_CLOSEOUT.md` — that spec is the authority, not the prior entry, since a fresh LOG file has none to copy.

---

# Filesystem name safety restarted from a baseline (2026-10-19)

**Session ID**: `361a54ac-98e8-48b2-98c4-1f68c080dcd2`

Rob Dickinson (robfromboulder), with Claude as co-author, reviewed PR #21 for #17, decided it had the wrong frame, and restarted the work as this item. The session landed a characterization pass of how every class of character in view names behaves today, closed #21 unmerged, and opened draft PR #27 against `v483`: a tests-first commit that fails on unmodified `v483`, then protections inside the filesystem storage client only.

## Lineage

- Rob ran a medium-effort code review of #21. It found that the blocklist sat in `ViewZooMetadata`, so it broke JDBC names that work; that `viewPath` still resolved untrusted names unchecked; that length limits counted characters, not bytes; and that test coverage was thin. Claude noted that the cache-before-storage finding is already PR #23's subject.
- Rob judged the compatibility risk larger than expected and proposed establishing a baseline of current behavior before deciding on protections. He also asked whether Windows mattered, having no Windows host to test on. Claude answered that Trino servers run on Linux, with macOS for development, so a claim of Linux and macOS support settles the drive-letter concern without Windows testing.
- Claude probed behavior directly instead of predicting it: a throwaway unit probe through `ViewZooMetadata` with the real filesystem client on macOS, then an integration probe through Trino 483 on Linux with Postgres, including a restart. The integration probe overturned two predictions:
  - Postgres rejects NUL.
  - A 100-character CJK name fails on Linux but succeeds on macOS.
- Claude wrote baseline tests asserting current behavior, with comments marking what looked wrong. Trial merges showed #23 and #21 both merge cleanly. #21 left the unit tests green, because its check sits above the client those tests drive, and failed 10 of 20 integration tests, which made its JDBC and backslash regressions concrete.
- Rob called a do-over:
  - Close #21 with an explanation.
  - Open a work item.
  - Land desired-behavior tests first, failing on unmodified `v483`.
  - Add protections aimed at filesystem storage on Linux and macOS, in a new draft PR referencing #17.

  Claude set the item up, converted the baseline assertions to desired behavior, and confirmed 6 unit and 5 integration failures on unmodified code. The protections then made all 35 unit and 20 integration tests pass. Rob later had the local baseline branch deleted, since #27 superseded it.

## Decisions

- Rob chose the do-over over reworking #21 in place, since #21's diff was small and its frame was wrong.
- Claude chose to keep `\`, `:`, Windows-reserved characters, control characters other than NUL, and non-ASCII accepted, because each round-trips on both platforms and through restart. Rejecting them would break working names for no filesystem reason.
- Claude applied the name rules only where a new file name is created (`createView` and the rename target), so views already stored under names now refused, such as long names on macOS, can still be dropped or renamed. The containment check in `viewPath` guards every operation.
- Claude enforced the 255-byte limit on macOS as well as Linux, so a view directory shared through git loads on both.
- Claude kept `INVALID_ARGUMENTS` for consistency with the existing name rules. Baseline tests do not assert cache state after a failed write, which keeps them independent of #23.

## What didn't work

- The first probe killed the surefire JVM at startup. Trino's TestNG services terminate the JVM when a test class name doesn't start with `Test`.
- The review predicted a Windows drive-letter escape. That escape is moot because the scope is Linux and macOS, and the escape that actually exists on those platforms is an absolute schema name.

## Open threads

- Remaining burndown: PR review, reviewer feedback, manual checks, closing #17 by hand after merge, and carrying forward to the next version branch.
- Whether to reject names that differ only in Unicode normalization remains open.

---

# PR #27 rebased onto merged #23 (2026-10-19)

**Session ID**: `2f960a1d-cdb0-4305-b6f7-d01e27140dbc`

Rob Dickinson (robfromboulder), with Claude as co-author, had PR #27 rebased onto `v483` after #23 (storage before cache in `createView` and `dropView`) merged in the same session. The rebase confirmed the earlier trial merge: no conflicts, and the item's tests still pass on top of #23.

## Lineage

- The session's main work was reviewing and merging #23, logged in the ViewZoo log. Once #23 merged, Claude flagged that this item's trial merge needed confirming against the real `v483`, and Rob asked for the rebase.
- Claude rebased both commits onto `v483` without conflicts, rebuilt the plugin, and ran the suites: 42 of 42 unit tests and 20 of 20 integration tests passed. Claude force-pushed `fs-safe-names` with lease, and GitHub reports #27 mergeable. It is still a draft.

## Open threads

- Remaining burndown is unchanged: PR review, reviewer feedback, manual checks, closing #17 by hand after merge, and carrying forward to the next version branch.

---

# Seven review rounds and Linux filesystem integration tests (2026-10-19)

**Session ID**: `cdd1a2f1-fb6b-46aa-92b4-425170479d78`

Rob Dickinson (robfromboulder), with Claude as co-author, ran seven medium-effort code reviews over PR #27 and had Claude fix the chosen findings after each, pushing eight commits to `fs-safe-names`. Filesystem storage now also rejects non-NFC names, refuses a create that the filesystem would store in another view's file, and skips with a warning any view file whose name Trino could not have created. A new `testfsmount` integration catalog measures filesystem behavior on Linux through a bind-mounted host directory. All 47 unit and 48 integration tests pass; PR #27 is open and no longer a draft.

## Lineage

- First review of the PR: Rob had Claude fix the README note, which claimed JDBC storage had none of the filesystem limits although it rejects NUL; add a test that reaches the containment check in `viewPath`, since every earlier rejection test was stopped by name validation first; and add cleanup so integration tests that create views can't leak them into each other. For the reported NFC/NFD collision on macOS, Rob chose to reject non-NFC names rather than normalize them.
- Second review: Claude showed that the claimed JDBC `VARCHAR(255)` limit is unreachable because `ViewZooMetadata` caps names at 100 characters; Rob still had the README document that cap. Rob had Claude handle non-NFC files already on disk and the reported final-sigma collision on case-insensitive APFS. Claude added a load-time name check that failed startup, and a case-fold rule built from Java's per-character mappings. The NFD load test had to be dropped because Java on macOS reports directory listings in NFC, so the connector never sees an NFD name there.
- Third review: the case-fold rule was wrong. APFS also folds `ß` to `ss` and `ﬀ` to `ff`, which the rule accepted (confirmed on this machine); the load check made uppercase file names such as `Sales.Report.json` fatal at startup; and Greek names ending in capital sigma became uncreatable because Trino lowercases them to final sigma. Claude proposed asking the filesystem instead of copying its rules, and Rob agreed: the case-fold rule and load check were removed, and `createView` refuses to write when the file exists but the directory listing doesn't hold that exact name.
- Fourth review: removing the load check let uppercase and NFD files load under lowercased names whose drop and replace miss the file. Claude recommended failing startup; Rob chose to skip such files with a logged warning, which added an explicit `io.airlift:log` dependency. Claude also switched the collision check to `toRealPath`, having verified only on macOS that it returns the stored name, and shortened lines to meet the 130-character limit.
- Fifth review: Rob asked Claude to re-verify before fixing. A probe in a Linux JVM against a case-insensitive bind mount showed `toRealPath` returns the requested name there, so the switch had broken collision detection on Linux; Claude restored the directory scan. Rob called the line-shortening edits a bad idea and had them reverted, and deferred the remaining error-reporting findings to #24.
- Rob then asked whether Claude was confident about macOS and Linux execution paths. Claude listed what had actually run: unit tests only on macOS, integration tests only on a case-sensitive container directory, and the collision check never on Linux. Rob proposed making Linux compatibility part of every integration run instead of relying on inspection and macOS semantics. Claude checked the Docker host first: OrbStack's kernel lacks Unicode casefolding, so neither casefold tmpfs nor casefold ext4 mounts, and a macOS bind mount is the only case-insensitive Linux directory available here.
- Claude added the `testfsmount` catalog, ran every SQL test against it as well, and added collision and skipped-file tests for both filesystem catalogs, with file probes run inside the Trino container. To show the tests catch regressions, Claude disabled the collision check and the load-time name check, saw three tests fail, and restored the source.
- Two further reviews found only test-harness issues: captured command output mixed in stderr, cleanup ignored failed deletes, the `/abs` row was missing for `testfsmount`, and the merged process helper lost streaming. A live check showed Trino logs entirely to stderr and Compose 5.5.0 merges it into the stdout of `docker compose logs`, so the log assertion now captures both streams. Claude rejected one finding as a false positive: files in the world-writable mount directory can be deleted by any user.
- Rob ruled HFS+ (NFD storage, UTF-16 length limit) a known issue not worth testing.

## Decisions

- Reject non-NFC names on create and rename (Rob), rather than normalizing them.
- Detect case and normalization collisions by comparing the exact directory listing, not by reproducing filesystem folding rules or by `toRealPath` (Claude proposed; Rob agreed).
- Skip and log view files whose names Trino could not have created, rather than failing startup (Rob, overriding Claude's recommendation).
- Measure filesystem behavior on Linux in the regular integration run (Rob).
- Don't restructure code or messages only to meet the 130-character line length (Rob).
- Error-reporting findings (dropped exception causes, a file deleted between the collision check and the write) go to #24 (Rob).

## What didn't work

- The case-fold rule and the `toRealPath` check both encoded platform behavior inferred from code or from macOS alone, and each had to be reverted one review later. The case-fold tests were deleted with the rule.
- The two connector commits around `toRealPath` changed almost no tests, and the existing collision test passed with both the broken and the fixed check because it only ran on macOS.

## Lessons

- Filesystem behavior is only as good as the tests that measure it; this PR needed tests of a kind the project didn't have before, not more of the same.
- Medium reviews returned six to ten findings every round, so the count never signals convergence; severity moved from connector data loss to test plumbing over the last two rounds.

## Open threads

- Rob plans to review the whole PR in a new session.
- The PR description predates this session and needs checking against the final code.
- Known gaps: a case-insensitive Linux directory is unmeasured on Linux hosts, HFS+ is untested, and #24 owns the deferred error reporting.
