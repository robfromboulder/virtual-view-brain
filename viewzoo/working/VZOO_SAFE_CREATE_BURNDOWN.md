# Safe Create: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `safe-create` off `v483`
  * commit changes on branch
  * create draft PR
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_SAFE_CREATE_CLAUDE.md`
  * manual checks — capture steps in `VZOO_SAFE_CREATE_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* after merge, run a one-off JaCoCo coverage report across unit and integration tests to find untested logic for the next hardening item; code inside the Trino container is counted only if the JaCoCo agent is added to that JVM
