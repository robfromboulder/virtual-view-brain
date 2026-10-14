# Modernize: Burndown

Everything between working code and a merged PR.

* carried over from `TRINO_483`, which merged in PR #10 and closed out before its release
  * run `./release.sh 483a` from `v483`, pull the image, and confirm a question in Claude Desktop calls the tools
  * in Claude Desktop with `test://complex_enterprise`, ask "what are the central hub views?" and confirm the tool-call panel shows ViewMapper and the answer lists centrality scores
  * in Claude Desktop with a `jdbc:trino://` connection to a live server, ideally older than 483, list catalogs and analyze a schema with views, and confirm the 483 driver connects without errors
  * fold both Claude Desktop checks into the MCP server's `TESTING.md`, with the rule that a check passes on numbers only a tool produces, since a model that skips tools still writes plausible prose
  * once `483a` is published, make `v483` the default branch
* PR wrangling
  * ~~create branch `modernize` off `v483`~~
  * commit changes on branch (ongoing)
  * ~~create draft PR against `v483`~~ — #11
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* system prompt audit
  * audit `ViewMapperAgent.SYSTEM_PROMPT` and the six tool descriptions for patterns written for older models, such as all-caps imperatives, "ALWAYS"/"NEVER" rules and step-by-step workflows the model would follow anyway
  * rewrite where it over-prescribes, keeping the size-band strategy and the discovery posture that the agent's approach puts in the prompt
  * agree an API spend budget with robfromboulder before any live run
  * run the same questions on all four datasets at `medium`, then at `low` and `high`, before and after the rewrite, and record tool calls, time and cost per question
  * a run passes only on output that only a tool produces, such as node IDs or centrality scores
  * set the default effort (open issue 1) from those numbers
* testing
  * automated checks — see `VMR_MODERNIZE_CLAUDE.md`
  * manual checks — capture steps in `VMR_MODERNIZE_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * reversal: the agent moved to `anthropic-java` 2.71.0, dropping LangChain4j (open issue 1, decided 2026-10-13)
  * the SDK builds a tool's schema from a Jackson-annotated class as strict, with every field required, and refuses a class with no fields; optional parameters (`limit`, `maxNodes`) now state their default in the description, and the two no-argument tools are declared from a hand-built `BetaTool`
  * `listSchemas` documented `catalog` as optional for catalog-bound connections, but both providers always required it, so strict mode changed nothing there
  * a refusal, a `max_tokens` stop, or a tool loop past 25 model calls now fails the run instead of returning partial text
* close #7 and #8 from the PR
* after merge, run `./release.sh` with the next letter, pull the image, and confirm a question in Claude Desktop calls the tools
