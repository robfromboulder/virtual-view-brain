# Security Mode: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `security-mode` off `v483`
  * commit changes on branch
  * create draft PR
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_SECURITY_MODE_CLAUDE.md`
  * manual checks — capture steps in `VZOO_SECURITY_MODE_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* carry the change forward when the next version branch is cut
