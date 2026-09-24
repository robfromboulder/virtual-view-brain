# ViewMapper: Scoping Statement

> V6, 2026-09-23.

This document defines the problem that ViewMapper addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states one part of the problem the ecosystem's scoping statement defines: the part where a hierarchy, once built, cannot be seen.

---

## 1. Problem Statement

A view hierarchy has no representation anywhere. Its dependencies exist only as table references inside SQL text, and the engine will show one definition at a time. Anyone who inherits a schema of any size is left reading definitions and holding the graph in their head.

Recovering that graph is necessary and not sufficient. A schema with thousands of views renders as a hairball that answers no question a person actually has, so the work does not end at extraction: it ends when someone can find a place to start, see a piece small enough to read, and move from there. That reframes the problem as guided exploration rather than diagram generation.

Accuracy carries unusual weight here. A map that cannot be trusted is worse than no map, because it will be believed.

---

## 2. State of the Problem

### What a person can get at today

Trino publishes what it knows about views through `information_schema.views`, one row per view, definition included as text. `SHOW CREATE VIEW` returns the same thing for a single view. Both are exact and neither is structural: obtaining the graph means reading every definition and reconstructing the edges between them by hand.

Nothing on the shelf does that reconstruction. ERD tools follow foreign keys and find nothing, because a view referencing another view leaves no constraint behind. General lineage tooling exists for warehouse pipelines and assumes a job graph or a modelling layer, neither of which is present when the hierarchy is just views in a query engine.

### What scale does to the question

Hierarchies reach hundreds or thousands of views in systems large enough to need this. At that size the question a person asks — "show me the schema" — has no useful answer: the complete picture is unreadable, and any subset requires knowing which subset, which is precisely what they do not know yet.

---

## 3. Goals

- Someone who inherits a view hierarchy learns its shape in minutes, starting without the name of a catalog or schema.
- At a scale where a complete picture is useless, the person still gets a useful answer rather than a refusal or a hairball.
- The dependencies a person acts on are the ones that exist.
- Orientation is never a reason to hesitate about pointing something at production.
- Conclusions drawn from the picture hold up against the schema itself.

---

## 4. What Is Not In Scope

- **Changing anything.** Understanding a hierarchy is the problem. Modifying one is not, and read-only is what makes the rest safe.
- **Column-level lineage.** The unit of dependency is the view, not the column.
- **Engines other than Trino.** Both the SQL dialect and the metadata surface are Trino's.
- **Replacing human review.** The output supports a judgment; it does not make one.

---

## 5. Open Questions

- Whether accuracy claims survive contact with a real thousand-view schema, and what happens to guided exploration at that size.
- Whether any of this holds against a Trino server with authentication enabled. Deployments large enough to have this problem are the ones most likely to require it, and nothing has established that the connection story works there.
- Whether a machine-produced map can be trusted for decisions at all, and what a person would have to see in order to verify one without redoing the work by hand.
