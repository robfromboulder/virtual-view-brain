# ViewMapper Agent: Technical Approach

> V3, 2026-08-02.

This document describes the proposed approach for addressing the problems defined in `VMR_AGENT_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

Give a language model a small set of precise tools and let it decide the sequence. The graph work — parsing, building, measuring, extracting — is deterministic Java that the model cannot get wrong by reasoning badly. What the model contributes is judgment about which of those operations the user's situation calls for, which is the part that resists being written as a fixed pipeline: whether a schema is small enough to draw whole, whether a chosen focus is still too big, whether the user needs discovery before analysis.

That division is the reason this is an agent rather than a program with an LLM-shaped front end. A fixed sequence would have to guess the user's intent from a single question; a reasoning loop can look at what it found, decide the answer would be useless, and do something else instead.

---

## 2. Architecture

A single Java process, invoked with a question and a connection, returning text. Inside it:

**A parser layer** turns each view definition into the set of tables and views it reads, using Trino's own SQL parser and walking the resulting syntax tree, so CTE names and string contents are excluded by construction rather than by pattern.

**A loading layer** obtains definitions either from a live server over JDBC or from a bundled dataset, behind one interface, so everything above it is indifferent to which.

**A graph layer** holds the dependency graph and answers structural questions about it: how large and tangled, which nodes are most depended upon, which have no dependents, which sit between the most others, and what lies within a given distance of a chosen node.

**A reasoning layer** exposes those operations to the model as tools and carries the instructions describing when to use them.

---

## 3. Key Design Decisions

**Trino's SQL parser, never regular expressions.** Regex cannot distinguish a table reference from a CTE alias, a quoted identifier, or a schema-qualified name inside a string literal, and each mistake is permanent in the resulting graph. Trino's parser is the authoritative reading of Trino SQL, and using anything else means reimplementing it worse.

**JGraphT for the graph, with the general directed graph type rather than the acyclic one.** The library brings proven implementations of the algorithms this needs, betweenness centrality included, which is not code worth writing. Choosing the general type over the DAG type is deliberate: real schemas occasionally contain cycles, and a DAG type would throw when an edge closed one — turning a schema quirk into a crash, on a tool whose job is to explain schemas. Traversals guard against revisiting, and centrality is well defined either way.

**LangChain4j for the model integration.** It supports Claude with function calling directly, registers tools by annotation, and abstracts the orchestration loop. It also allows a test model implementation to be substituted for the real one, which is what makes the reasoning layer testable without spending tokens.

**The system prompt encodes the exploration strategy, not just tool descriptions.** It tells the model to assess complexity first, and what to do at each size band: draw the whole thing when it is small, suggest grouping when it is medium, and guide toward entry points when it is large. It also states the discovery posture — that most users connect without naming a catalog, and that discovery is cheap enough to offer proactively. The strategy lives here rather than in code because it is guidance, not control flow: the model is expected to depart from it when the situation calls for it.

**Connections are stateless and unpooled.** Each invocation opens what it needs and exits. For a tool invoked a handful of times per exploration this costs a connection setup and saves a lifecycle to get wrong.

**Nothing is cached or precomputed between invocations.** Every question re-reads the schema, re-parses every definition, and recomputes whatever graph measures it needs. This follows from the module answering one invocation at a time, and it holds because the measured cost of doing so stays inside what a person will wait for at the sizes reached so far. It is the first decision that breaks if a schema is large enough that parsing and centrality no longer fit in that budget, and the remedy at that point is caching rather than a different design.

**Discovery mirrors live and test sources exactly.** A bundled dataset presents as a catalog named `test` with the datasets as its schemas, so exploring test data and exploring a real server are the same conversation. A user does not need to know which they are on.

---

## 4. What We Build

A Java command-line program that connects to Trino or a bundled dataset, extracts an accurate dependency graph from view definitions, analyzes that graph, and drives a Claude model through six tools — two for discovery, four for analysis — to produce guided answers and Mermaid diagram source as text on standard output.
