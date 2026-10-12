# Trino 483: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * cut `v479` from the tip of `main`, push it, and make it the default branch
  * cut `v483` from `v479` and push it
  * create branch `trino-483` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VMR_TRINO_483_CLAUDE.md`
  * manual checks — capture steps in `VMR_TRINO_483_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* after merge, run `./release.sh 483a` and pull the image to confirm it
* once `483a` is published, make `v483` the default branch
