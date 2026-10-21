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
  * the scope fix also dropped `byte-buddy`, which only `configuration-testing` pulled in, shrinking the release zip from about 15 MB to 12 MB
  * the README installs with a curl script that finds the newest `483<letter>` release through GitHub's API, rather than a manual download, and doesn't check the SHA-256
  * the release procedure computes no checksum and the release notes carry none, since the README doesn't check it and GitHub shows each asset's SHA-256 (Rob)
