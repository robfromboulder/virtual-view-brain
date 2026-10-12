# Modernize: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `modernize` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VMR_MODERNIZE_CLAUDE.md`
  * manual checks — capture steps in `VMR_MODERNIZE_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* close #7 and #8 from the PR
* after merge, run `./release.sh` with the next letter, pull the image, and confirm a question in Claude Desktop calls the tools
