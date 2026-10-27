# Virtual View: Scoping Statement

> V7, 2026-10-26.

This document defines the problem that the virtual view ecosystem addresses, separately from design decisions and implementation details, as an objective and unbiased resource.

---

## 1. Problem Statement

SQL views can serve as an application's data contract: layers of views standing between the application and physical storage, each replaceable without disturbing the layers above it or the queries in flight. This problem belongs to teams that run Trino and want views as that contract; both are given. Query engines make the pattern possible without making it practical. The engine treats each view as an isolated object, so everything that turns a pile of views into an architecture — the conventions, the shape of the hierarchy, the place the definitions live — falls to whoever adopts the pattern.

Three obstacles therefore stand between a team and the pattern, and clearing one leaves the others in place. The practice is unwritten, so each team invents its own conventions and finds the sharp edges by hitting them. A hierarchy is invisible once built, because its dependencies exist only inside SQL text that the engine will show one view at a time. And the definitions need somewhere to live, which normally means adopting storage infrastructure heavier than the pattern it would support.

---

## 2. State of the Problem

This assessment is as of October 2026.

### What a team can use today

**Doing it ad hoc.** Each team writes views as it goes, keeps its conventions in its head, reads `SHOW CREATE VIEW` one definition at a time to understand a hierarchy, and stores views wherever its data already lives. It costs nothing new where a Hive metastore already runs, and leaves all three obstacles in place.

**An Iceberg catalog.** Trino-native storage for views beside Iceberg tables, needing a catalog service and object storage or a shared file system. For a team already running one, it removes the storage obstacle at no extra cost. It leaves the practice unwritten and the hierarchy invisible.

**dbt.** Views become models in a git repository, with folder and naming conventions, generated documentation and a lineage graph, deployed to Trino through the dbt-trino adapter. It addresses all three obstacles with one adopted tool. The cost is a build tool and a Python toolchain beside the engine, conventions shaped for transformation pipelines rather than for views as an application's contract, and a deployment run between a changed definition and a replaced view. The views still need a connector to live in.

**Data catalogs (DataHub, OpenMetadata).** A catalog platform ingests Trino's metadata, parses view definitions into a lineage graph, and shows it in a web interface. It makes any hierarchy visible, at the cost of deploying and operating the platform, and leaves the practice and storage as they were.

### What the engine provides

Trino supports the mechanics. `CREATE OR REPLACE VIEW` is what makes a layer swappable at runtime, and it works. What it does not do is check the replacement: Trino validates no column types when a view is replaced and offers no locking, so a definition can change under a hierarchy and the resulting breakage surfaces later, at query time. Queries already running keep the definition they were planned against.

That behavior is a platform property rather than a standardized one. ANSI/ISO SQL assumes a view definition is frozen at creation and changed only during downtime, so the runtime replacement this pattern depends on varies between engines and is guaranteed by none of them.

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

- **Platforms other than Trino.** The teams with this problem run Trino. Other engines with SQL views may have the same problem, but it is not the one stated here.
- **Table storage.** The subject is view definitions. Tables, materialized views, and the physical data underneath stay with whatever system already holds them.
- **Displacing ORMs or microservices.** Where all data access already flows through application code, the pattern adds nothing. It targets SQL-native systems and coexists with the alternatives elsewhere.
- **Engine changes.** Teams with this problem run Trino as released, so the answer cannot depend on modifying it.

---

## 5. Open Questions

- Whether the owners of a hierarchy can keep it intact without help from the engine. Views replace with no type checking and no locking, so the discipline rests entirely on them, and it is untested whether that holds in a system large enough to matter.
- Whether the three obstacles above are what actually blocks adoption. The evidence is anecdotal, and no account exists of a team taking up the pattern end to end.
- Where the boundary sits between a virtual view and a materialized view. Caching results changes the replacement story.
