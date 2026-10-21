# Security Guide: Session Log

Running log of implementation sessions. Each session appends after a `---` separator.

The first entry, and every one after it, follows the entry format and content rules in `VV_SESSION_CLOSEOUT.md` — that spec is the authority, not the prior entry, since a fresh LOG file has none to copy.

---

# Draft the security guide and open its PR (2026-10-20)

**Session ID**: `34ab1b70-b72b-480e-84f3-137278163584`

Rob Dickinson (robfromboulder) asked Claude to read this work item and draft `SECURITY.md`. The session checked the plan's claims against `v483`, wrote the guide plus a README badge on a new `security-guide` branch in its own worktree, corrected this item's findings and plan to match the code, and opened draft PR #37 against `v483`.

## Verifying the plan against the code

Rob directed mid-session that the code is ground truth wherever it and the work-item docs disagree. Three of the plan's premises had gone stale on `v483`:

- A file or row that fails to parse no longer stops the catalog loading: both storage clients' `getViews` skip it and log a warning. The plan's `VZOO_STORAGE_ERRORS` risk row was moot.
- A name containing `/` can't escape `viewzoo.dir`: filesystem storage rejects `/` and NUL in names, and `viewPath` refuses any path whose parent isn't the directory. The path-safety open issue closed with no vulnerability to fix.
- The Jackson cap is real. The plugin bundles jackson-core 2.22.1, whose default `StreamReadConstraints` cap a string at 20,000,000 characters with no document-length limit. A standalone probe against the bundled jars showed a string one past the cap serializes fine and fails to read with `StreamConstraintsException`, an `IOException`, so a view with SQL that long is stored, keeps working until the next restart, and is then skipped with a warning.

One property the docs missed: `ViewZooMetadata` is a Guice singleton that reads storage only in its constructor, so an edit made directly to storage takes effect only at the next restart. The guide states this alongside the point that whoever can write storage controls the owner a `DEFINER` view runs as.

## Decisions

- **Supported versions:** Claude wrote "only the newest version branch receives fixes" into the guide and the findings. Rob hasn't confirmed it explicitly; the draft PR is where it gets reviewed.
- **README link:** a Security badge after License, matching the existing Contributing badge, rather than prose that would collide with the `VZOO_WHY_VIEWZOO` README rework.
- **Worktree:** Rob was working on `why-viewzoo` in another session from the main checkout, so at Rob's request this work moved to a separate worktree at `../viewzoo-security-guide` and the session switched into it. The branch's upstream to `origin/v483` was unset so a plain push can't land on `v483`.

## Repository state found

The default branch is still `v479`. Private vulnerability reporting is off, though the guide links to it. Dependabot security updates are off. Secret scanning and push protection are on.

## Still open

Turn on private vulnerability reporting before merge, then Dependabot alerts and code scanning default setup. Rob will review the PR text, including the supported-versions policy.
