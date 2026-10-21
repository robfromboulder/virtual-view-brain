# Security Guide: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `security-guide` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review doc changes
  * full rebuild and automated retest on PR code
  * review PR description against final docs one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_SECURITY_GUIDE_CLAUDE.md`
  * manual checks — capture steps in `VZOO_SECURITY_GUIDE_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * on `v483`, malformed files and rows are skipped with a warning (not catalog-fatal), and names that would escape `viewzoo.dir` are rejected; the guide documents both
  * the supported-versions policy (newest branch only) was chosen by Claude, pending Rob's review on PR #37
* repository settings: private vulnerability reporting, Dependabot alerts, code scanning default setup
