# Virtual View: Scoping Statement

> V5, 2026-08-02.

This document defines the problem that the virtual view ecosystem addresses, separately from design decisions and implementation details, as an objective and unbiased resource.

---

## 1. Problem Statement

SQL views can serve as an application's data contract: layers of views standing between the application and physical storage, each replaceable without disturbing the layers above it or the queries in flight. Query engines make this possible without making it practical. The engine treats each view as an isolated object, so everything that turns a pile of views into an architecture — the conventions, the shape of the hierarchy, the place the definitions live — falls to whoever adopts the pattern.

Three obstacles therefore stand between a team and the pattern, and clearing one leaves the others in place. The practice is unwritten, so each team invents its own conventions and finds the sharp edges by hitting them. A hierarchy is invisible once built, because its dependencies exist only inside SQL text that the engine will show one view at a time. And the definitions need somewhere to live, which normally means adopting storage infrastructure heavier than the pattern it would support.

---

## 2. State of the Problem

### What the engine provides

Trino supports the mechanics. `CREATE OR REPLACE VIEW` is what makes a layer swappable at runtime, and it works. What it does not do is check the replacement: Trino validates no column types when a view is replaced and offers no locking, so a definition can change under a hierarchy and the resulting breakage surfaces later, at query time. Queries already running keep the definition they were planned against.

That behavior is a platform property rather than a standardized one. ANSI/ISO SQL assumes a view definition is frozen at creation and changed only during downtime, so the runtime replacement this pattern depends on varies between engines and is guaranteed by none of them.

### What the literature provides

Standard guidance treats views as decoration — hiding joins, computing columns, restricting access — and stops there. The architectural use has no canonical description, no named conventions, and no accounting of its failure modes. A practitioner evaluating it is comparing an undocumented pattern against ORMs, microservices and data access layers, all of which are thoroughly written up.

### What a built hierarchy exposes

Nothing that shows its shape. Dependencies exist only as table references inside SQL text; `SHOW CREATE VIEW` returns one definition at a time; and ERD tools trace foreign keys, which view-to-view dependencies do not have. Recovering the graph means reading every definition in the schema and reconstructing the edges by hand.

### Where definitions can live

Every view definition must be persisted by some connector, and the connectors that can hold them bring infrastructure with them: a Hive-compatible metastore, or object storage plus a table format. That is a deployment to secure, back up and upgrade in exchange for storing a modest amount of SQL text. The cost is most conspicuous exactly where the pattern is most useful — a view over static values has no data source to sit beside, and a team prototyping has not yet chosen a database at all.

### Evidence that the problem is real

It is thin, and it is not nothing. Practitioners report using these patterns in production and send feedback on them, and teams have built private tooling against these obstacles rather than wait for a public answer.

---

## 3. Goals

- A practitioner can judge whether the pattern fits their system, and apply it without inventing conventions or rediscovering the sharp edges.
- Someone who inherits a view hierarchy can learn its shape without reading every definition in it.
- Persisting a view definition does not require adopting infrastructure beyond what the system already runs.
- Clearing one obstacle is enough to keep going: no remaining gap blocks a team that has cleared the others.

---

## 4. What Is Not In Scope

- **Platforms other than Trino.** The pattern ports to any engine with SQL views, and Starburst Enterprise and Galaxy will run all of this. None of them is documented, tested or supported, and no claim about their behavior is made.
- **Table storage.** The subject is view definitions. Tables, materialized views, and the physical data underneath stay with whatever system already holds them.
- **Displacing ORMs or microservices.** Where all data access already flows through application code, the pattern adds nothing. It targets SQL-native systems and coexists with the alternatives elsewhere.
- **Engine changes.** Nothing here proposes modifying Trino. The pattern is built from what the engine already does.

---

## 5. Open Questions

- Whether guidance is enough where the engine will not help. Views replace with no type checking and no locking, so the discipline that keeps a hierarchy intact rests entirely on its owners, and it is untested whether that holds in a system large enough to matter.
- Whether the three obstacles above are what actually blocks adoption. The evidence is anecdotal, and no account exists of a team taking up the pattern end to end.
- Where the boundary sits between a virtual view and a materialized view. Caching results changes the replacement story, and the pattern currently sidesteps the question by staying with plain views.
