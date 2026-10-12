# Release Binaries: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `release-binaries` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_RELEASE_BINARIES_CLAUDE.md`
  * manual checks — capture steps in `VZOO_RELEASE_BINARIES_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* after merge, push tag `483a` and confirm the release and its archive
* once `483a` is published, switch the GitHub default branch from `v479` to `v483`
* delete the test fork's tags and releases
* carry the workflow forward to each new version branch
