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
  * decide whether the README should say filesystem storage needs hard links, which create now requires as rename already did
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * deviation: the `replace` plumbing landed in the failing-tests commit, since the tests can't compile against the old signature
  * deviation: the partial-write case is covered by making the directory read-only (`testReplaceDoesNotWriteInPlace`), not by simulating a full disk
  * deviation: the README is unchanged, since it states no filesystem requirements
  * reversal: see the Reversals section of `VZOO_SAFE_CREATE_FINDINGS.md`
* after merge, run a one-off JaCoCo coverage report across unit and integration tests to find untested logic for the next hardening item; code inside the Trino container is counted only if the JaCoCo agent is added to that JVM
