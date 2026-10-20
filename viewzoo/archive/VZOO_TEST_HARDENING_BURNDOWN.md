# Test Hardening: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `test-hardening` off `v483`
  * commit changes on branch
  * create draft PR
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_TEST_HARDENING_CLAUDE.md`
  * manual checks — capture steps in `VZOO_TEST_HARDENING_TESTING.md`
  * rerun the coverage measurement and confirm each gap in `VZOO_TEST_HARDENING_FINDINGS.md` is covered
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * coverage after the work: 98.9% of lines and 97.8% of branches, up from 92% and 93%
  * deviation: the decision record's list of paths that can't happen missed `viewPath`'s `InvalidPathException` catch, which stays uncovered because names are validated before a path is built
