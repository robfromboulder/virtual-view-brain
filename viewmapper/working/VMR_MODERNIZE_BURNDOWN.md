# Modernize: Burndown

Everything between working code and a merged PR.

* carried over from `TRINO_483`, which merged in PR #10 and closed out before its release
  * run `./release.sh 483a` from `v483`, pull the image, and confirm a question in Claude Desktop calls the tools
  * in Claude Desktop with `test://complex_enterprise`, ask "what are the central hub views?" and confirm the tool-call panel shows ViewMapper and the answer lists centrality scores
  * in Claude Desktop with a `jdbc:trino://` connection to a live server, ideally older than 483, list catalogs and analyze a schema with views, and confirm the 483 driver connects without errors
  * fold both Claude Desktop checks into the MCP server's `TESTING.md`, with the rule that a check passes on numbers only a tool produces, since a model that skips tools still writes plausible prose
  * once `483a` is published, make `v483` the default branch
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
