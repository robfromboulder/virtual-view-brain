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
