# Security Guide: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `security-guide` off `v479`
  * commit changes on branch
  * create draft PR against `v479`
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
* repository settings: private vulnerability reporting, Dependabot alerts, code scanning default setup
* carry `SECURITY.md` forward to each new version branch, so the default branch always has it
