# ViewMapper Agent: Implementation Findings

> V2, 2026-08-02.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## Three layers were built and then removed

An earlier structure put a service class between the command entry point and the agent, wrapped the agent's answer in a result type, and held exploration state in a context object of its own. All three came out, leaving the command calling the agent directly, the agent returning a plain string, and conversation state living inside the model integration where it already existed.

Each removal had the same shape: the layer existed to hold something that turned out to have a home already. The service class held no logic the command did not; the result wrapper carried one string; the context object duplicated memory the agent framework maintains. What looks like an unusually flat call path is the residue of taking those out, not an absence of design — anyone tempted to reintroduce an orchestration layer here should know it was tried.

## Trino lowercases unquoted identifiers, and tests have to agree

Identifiers that arrive unquoted are normalized to lowercase before anything downstream sees them, so a view written as `MyView` is `myview` by the time it reaches the graph. Quoting preserves case. This is invisible in ordinary use and shows up as tests that pass or fail depending on how their fixtures were written, so test data has to make the choice deliberately rather than by accident.

## The schema argument is split on its first period, not its last

A schema argument may be `catalog.schema` or a bare schema name depending on whether the connection URL bound a catalog. The split takes the first period, which means a catalog containing a period would be parsed wrongly and a schema containing one is handled correctly. This asymmetry is deliberate and worth knowing before anyone "fixes" the split direction.

## Cycles are tolerated, not endorsed

The graph type accepts cycles because real schemas occasionally contain them, and traversals guard against revisiting rather than assuming acyclicity. Nothing reports a cycle to the user. A cycle in a view hierarchy almost always indicates a mistake in the hierarchy, so the current behavior is silence about a real problem rather than correct handling of a normal case.
