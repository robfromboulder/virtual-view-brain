# Security Guide: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout each check folds into the project repo `CLAUDE.md` of the lobe it exercises.

## Setup

`v483` is the repository's default branch.

## Test cases

1. **Security tab** — open the repository's Security tab.
   - **Expected:** it shows `SECURITY.md`.
2. **Claims match the code** — check each statement in `SECURITY.md` against the code on `v483`.
   - **Expected:** every statement holds.
3. **Repository settings** — open the repository's security settings.
   - **Expected:** private vulnerability reporting, Dependabot alerts and code scanning default setup are on.
