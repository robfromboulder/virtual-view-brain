# ViewZoo: Technical Approach

> V3, 2026-08-02.

This document describes the proposed approach for addressing the problems defined in `VZOO_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

Be a connector that stores views, and be unremarkable about it. Everything a user does here is ordinary Trino SQL against ordinary Trino views, and the only unusual thing about the catalog is where the definitions ended up. That is the whole product claim: adopting this should be a configuration file, not a technique.

The two environments are served by two storage backends rather than by one compromise. Files on disk suit development, testing and version control, because a JSON file per view is something a person can read, a repository can hold, and a pull request can review. A database suits production, because it survives containers being replaced, is reachable from every node, and is already in the backup schedule. Neither is a degraded version of the other, and the choice is a configuration property.

---

## 2. Architecture

The plugin registers a connector factory, which builds a connector through a Guice module that reads configuration and wires the pieces as singletons. The connector supplies a metadata component, and that component is where every view operation lands: create, replace, drop, list and get.

Underneath it sits one storage interface with two implementations, selected at startup by a provider that reads the configured storage type. The filesystem implementation writes one JSON file per view, named for its schema and view. The JDBC implementation writes rows into a table in PostgreSQL. Nothing above the interface knows which is in use.

The metadata component holds every view in memory, loaded once at startup, and serves reads from there. Configuration is declared in typed classes using the Airlift framework, with credentials marked sensitive so they stay out of logs.

---

## 3. Key Design Decisions

**A storage interface with a runtime-selected implementation.** The alternative — two connectors, or one connector with conditionals threaded through it — would duplicate the view logic or tangle it. One interface keeps all view semantics in one place, and makes a third backend a matter of writing one class.

**Views are stored as Trino's own serialized view definition.** Using Trino's model rather than a bespoke format means a stored view is exactly what Trino would have held anyway, with no translation layer to drift and no fidelity to lose on round trips.

**The store holds what it is given and judges none of it.** Whatever Trino hands over is persisted and returned unchanged, including the view's security mode, which is carried rather than checked. This is the current answer to whether a view store is storage or governance, and it is the reason a request to enforce a security mode is a change of position rather than a feature: enforcing anything means the store starts having opinions about the views it holds, and every such opinion is a way for a stored view and a Trino view to stop being the same thing.

**Everything is cached in memory, loaded once at startup, and never watched.** This makes reads immediate and the implementation small, and it assumes storage changes only through this connector. The assumption is wrong in one real workflow — definitions synchronized into a directory from git — and the resulting need for a restart is the most substantive open request from users. Any change here trades the current guarantee that memory and storage agree.

**View operations are synchronized.** Metadata methods are serialized rather than made concurrent. For a workload of occasional DDL against a small in-memory map, correctness is worth more than the throughput given up, and it removes an entire class of bug from a connector whose failure mode would be losing view definitions.

**A branch per Trino version, with `main` effectively unused.** Trino numbers releases without semantic versioning and can break plugin interfaces in any of them, so a branch is compatible with exactly one Trino release. New branches are cut from the previous branch and never merged back, and contributions target a version branch. The cost is that fixes must be carried forward by hand; the benefit is that a user on an older Trino has something that actually compiles against it.

**Filesystem storage is treated as a feature, not a fallback.** Views as JSON files in a directory means view definitions can live in a repository with history, review and branching — the same handling as application code, without a database or a file share. This is the reason the filesystem backend exists alongside the database one rather than being a development shortcut.

---

## 4. What We Build

A Trino plugin providing a catalog whose views are stored either as JSON files in a configured directory or as rows in a PostgreSQL table, chosen by one configuration property, requiring no metastore and no object storage, and behaving as ordinary Trino views in every other respect.
