# ViewMapper Agent: Scoping Statement

> V5, 2026-08-02.

This document defines the problem that the agent addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states the analytical half of the problem ViewMapper's scoping statement defines.

---

## 1. Problem Statement

Turning a Trino schema into a dependency graph, and then answering questions about that graph well enough to guide someone through it.

Extraction is the part that looks easy and is not. A view's dependencies are the tables and views its definition actually reads, which is not the same as the identifiers appearing in its text: a CTE name is not a table, a schema-qualified name inside a string literal is not a reference, and subqueries, unions and quoted identifiers each break the naive reading in their own way. Getting this wrong is expensive at scale, because a graph is a structure where local errors have global effects — one spurious edge changes which views look central, which look isolated, and what any focused subgraph contains.

Answering questions about the graph is a second problem. "Show me the schema" is not answerable for a schema of any size; what a person needs is a judgment about whether the thing is small enough to see whole, and if not, a short list of places worth starting from and a way to pull back a piece around one of them. Those are graph-analysis questions, and they have to be answered before any rendering decision can be made.

The analysis also has to stand alone, without a conversation wrapped around it. That is what makes it verifiable, and what keeps it usable by callers other than a conversational one.

---

## 2. State of the Problem

### What Trino gives an analyzer to work with

One query against `information_schema.views` returns every view in a schema with its definition as text. That is the whole input: no dependency metadata, no structure, no ordering. Everything about the graph has to be derived from the SQL.

Trino also publishes the parser it uses to plan queries. Anyone parsing Trino SQL has a choice between that parser, which is authoritative by construction, and an approximation that will disagree with the engine somewhere.

### What makes the SQL hard to read correctly

The gap between "identifiers in the text" and "tables actually read" is where the errors live. Common table expressions introduce names that look qualified and refer to nothing outside the statement. String literals contain schema-qualified text that matches any pattern written to find references. Subqueries nest scopes. Quoted identifiers preserve case and punctuation that unquoted ones do not, and Trino lowercases the unquoted ones, so two spellings of the same name are the same object while two spellings of another are not.

### What the graph is actually like

Directed, and not reliably acyclic. Real schemas occasionally contain cycles, rarely and usually by mistake, which means any analysis that assumes a DAG will fail on precisely the schemas most in need of explanation.

The questions people bring to it are structural and standard: what is most depended upon, what has no dependents, what sits between the most others, and what lies within a given distance of a chosen node. General graph theory already answers these; whether its notion of importance matches a view hierarchy's notion is a separate matter.

### What scale demands

Hierarchies reach thousands of views where this problem is worth solving, so the practical constraint is that parsing every definition and computing centrality over the result has to complete while someone waits for an answer.

### Where the question comes from

The person asking usually cannot name a catalog or schema when they start, so an analyzer that requires those as inputs is unusable at the moment of first contact.

---

## 3. Goals

- The dependencies attributed to a view are the ones it reads, on SQL that uses CTEs, subqueries, unions, quoted identifiers and string literals containing plausible-looking names.
- Whether a schema can usefully be shown whole is established before anything is produced, and governs what happens next.
- A person with no idea where to begin is given somewhere to begin, and the suggestions are ones a knowledgeable colleague would make.
- A person who names one view can get back a piece of the graph scoped to how far they want to look in each direction.
- Someone who knows no catalog or schema names can still start.
- A cyclic schema is explained rather than rejected.
- Analysis can be exercised and verified on its own, with no conversational layer involved.

---

## 4. What Is Not In Scope

- **Column-level lineage.** The unit of dependency is the view.
- **Conversation.** Holding a thread across questions is not this module's problem.
- **Writing to Trino.** No DDL, no DML.
- **Non-Trino SQL.** Accuracy rests on Trino's own dialect being the one in front of it.
- **Displaying anything.** Producing diagram content is in scope; rendering it is not.

---

## 5. Open Questions

- Whether parsing coverage has gaps that only appear on real-world SQL. `exclude_columns` is one known variation with nothing exercising it, and it is unlikely to be the only one.
- Whether betweenness centrality is the right notion of "worth starting from" for view hierarchies specifically, or a reasonable default borrowed from general graph analysis.
- Whether cycles should be reported as findings rather than merely tolerated, given that they usually indicate a design problem in the hierarchy.
- Whether an interactive rendering — a notebook, or something else a reader can manipulate — would serve exploration better than a static picture.
