# ViewMapper Agent: Implementation Findings

> V4, 2026-10-13.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## Three layers were built and then removed

An earlier structure put a service class between the command entry point and the agent, wrapped the agent's answer in a result type, and held exploration state in a context object of its own. All three came out, leaving the command calling the agent directly, the agent returning a plain string, and conversation state living inside the model integration where it already existed.

Each removal had the same shape: the layer existed to hold something that turned out to have a home already. The service class held no logic the command did not; the result wrapper carried one string; the context object duplicated memory the agent framework maintains. What looks like an unusually flat call path is the residue of taking those out, not an absence of design — anyone tempted to reintroduce an orchestration layer here should know it was tried.

## Trino lowercases unquoted identifiers, and tests have to agree

Identifiers that arrive unquoted are normalized to lowercase before anything downstream sees them, so a view written as `MyView` is `myview` by the time it reaches the graph. Quoting preserves case. This is invisible in ordinary use and shows up as tests that pass or fail depending on how their fixtures were written, so test data has to make the choice deliberately rather than by accident.

## The schema argument is split on its first period, not its last

A schema argument may be `catalog.schema` or a bare schema name depending on whether the connection URL bound a catalog. The split takes the first period, which means a catalog containing a period would be parsed wrongly and a schema containing one is handled correctly. This asymmetry is deliberate and worth knowing before anyone "fixes" the split direction.

## The default model is a Sonnet because Haiku would not reliably call tools

Haiku was tried and did not consistently invoke the tools it was given. For this module that is not a quality gradient but a total failure: every useful answer depends on the model choosing to call something, so a model that declines to call anything returns confident prose about a schema it never read. Anyone changing the default, or pointing the model override at something cheaper, has to verify tool invocation specifically — the prose looks equally plausible either way, which is what makes the failure easy to miss.

## The costs that justify recomputing everything were measured at 154 views

Nothing is cached between invocations, and the measurements behind that are: parsing 154 view definitions under 500ms, building the full graph under 100ms, betweenness centrality over 154 nodes under 200ms, and subgraph extraction under 10ms. That is also the largest schema these were taken on, so they establish that the work is effectively free at that size and say nothing about the thousands-of-views case. Centrality is the term that grows fastest and is therefore the one to re-measure first when a larger schema becomes available.

## Cycles are tolerated, not endorsed

The graph type accepts cycles because real schemas occasionally contain them, and traversals guard against revisiting rather than assuming acyclicity. Nothing reports a cycle to the user. A cycle in a view hierarchy almost always indicates a mistake in the hierarchy, so the current behavior is silence about a real problem rather than correct handling of a normal case.

## A tool's parameters are whatever the model's JSON can build

The model calls a tool with JSON arguments, which the integration framework deserializes into the method's parameters. A parameter type Jackson cannot construct makes the tool uncallable: the focused-diagram tool took a subgraph result type with no usable creator, and every focused diagram failed from at least 479 until ViewMapper PR #10 changed it to take the focus view and depths. Unit tests that call a tool method directly skip that layer, so each tool needs at least one test that goes through the framework's tool executor with JSON arguments. Parameter names reach the model only when the module compiles with `-parameters`; without it the model sees `arg0` upward, all required. Dumping the generated tool specifications from jshell on the module's classpath shows exactly what the model receives.

## The output-token cap does not follow the model

The cap is fixed at 16000 because the framework's default of 1024 cuts long Mermaid diagrams short. Some Claude models have a lower output limit, and robfromboulder declined to make the cap depend on the model: a model change is unlikely, and if one happens, a request rejected outright is better than a diagram truncated quietly.

## A Trino upgrade is checked against the visitor's method list

The dependency extractor relies on Trino's default traversal visitor, so what a new Trino version finds depends on which nodes that visitor descends into. Listing the visitor's methods with `javap` on the new parser JAR answers that faster than the release notes do. That is how the 483 upgrade found that table-function `TABLE(...)` arguments fell through to a no-op (#3), and that the left-hand value of an `IN` predicate had moved to a node the visitor already traverses.

## A CTE's visibility of its own name was not checked against Trino

The extractor treats a non-recursive CTE's own name, inside its body, as a reference to a real table, and treats a recursive one's as the CTE. A test encodes that rule, which was never checked against a live Trino.
