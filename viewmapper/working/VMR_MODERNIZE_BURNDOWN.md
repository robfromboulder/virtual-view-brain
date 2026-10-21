# Modernize: Burndown

Everything between working code and a merged PR.

* carried over from `TRINO_483`, which merged in PR #10
  * in Claude Desktop with `test://complex_enterprise`, ask "what are the central hub views?" and confirm the tool-call panel shows ViewMapper and the answer lists centrality scores
  * in Claude Desktop with a `jdbc:trino://` connection to a live server, ideally older than 483, list catalogs and analyze a schema with views, and confirm the 483 driver connects without errors
  * fold both Claude Desktop checks into the MCP server's `TESTING.md`, with the rule that a check passes on numbers only a tool produces, since a model that skips tools still writes plausible prose
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
  * the image moved to `ubuntu:resolute-20260927` (26.04 LTS), whose archive carries Python 3.14 and OpenJDK 25, so the deadsnakes and Adoptium repositories are gone; the 26.04 base lacks `addgroup` and blocks system `pip`, so the Dockerfile uses `groupadd`/`useradd -m` and a venv
  * the image grew from 671MB to 792MB, mostly from a larger base layer and the agent JAR gaining 43MB of SDK dependencies (Kotlin runtime, OkHttp, JSON schema generator)
  * MCP SDK 2.x removed the low-level `Server`'s `@list_tools`/`@call_tool` decorators: handlers are now passed to the constructor, take `(ctx, params)` and return `ListToolsResult`/`CallToolResult`, and model fields are snake_case (`input_schema`, `is_error`); every failed call now returns `is_error=True`, and a new stdio test checks it on the wire
  * the Trino driver only parses the URL in `getConnection` and connects on the first query, so `RunCommand` reports a `getConnection` failure as a malformed URL and a network cause on the first query as an unknown host, refused connection or timeout; messages name only host and port, and strip the URL from the driver's text, because a URL can carry a password
  * an unroutable host takes about 2 minutes to fail, because the driver retries; its `timeout` URL property doesn't shorten this (12 attempts over 2.1m at `timeout=10s`)
  * `RunCommandJdbcTest.testTestDatasetStillWorks` ran the real agent, making a paid API call whenever `ANTHROPIC_API_KEY` was set; replaced by `testTestConnectionStringAccepted`, which uses a missing dataset to stop before the agent, so the suite now runs free with a key set
* close #7 and #8 from the PR
