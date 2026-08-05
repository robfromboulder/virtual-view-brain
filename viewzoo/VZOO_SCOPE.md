# ViewZoo: Scoping Statement

> V5, 2026-08-02.

This document defines the problem that ViewZoo addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states one part of the problem the ecosystem's scoping statement defines: the part where view definitions need somewhere to live.

---

## 1. Problem Statement

A view definition has to be persisted somewhere, and Trino's answer is to store it in a connector that also stores data. That is fine when the data already lives in one, and awkward in the cases that matter most here. A view backed entirely by static values has no data source to be stored beside. A team prototyping has not chosen a database yet, and picking one to hold views is the commitment the pattern was supposed to defer. A team that wants views under version control finds them locked inside a metastore instead.

The available options are heavier than the need. A Hive-compatible metastore, or an object store plus a table format, is infrastructure to deploy, secure, back up and upgrade — for what is, in the end, a small pile of SQL text. The gap is a place to keep view definitions that costs nothing to run and can be adopted before anything else has been decided.

Storage is not one problem, though, because the environments differ. A developer wants files they can read, diff, review and throw away. A production cluster wants something that survives container replacement, is shared across nodes, and lands in the backups that already exist. Serving one of those well and the other badly leaves the pattern half-supported.

---

## 2. State of the Problem

### What Trino requires of a view store

Views live in catalogs, and a catalog is a connector. Any connector holding views must implement the metadata operations Trino calls to create, replace, drop, list and read them, and must persist what Trino hands it faithfully enough that the view comes back unchanged. The connector interface is where this is decided; there is no view storage outside it.

Trino's plugin interface is not stable across releases. Releases carry major numbers only, without semantic versioning, and any of them can break a plugin, so anything built against this surface is compatible with the release it was built against and no other.

### What is available to store views in

The connectors that can hold views are the ones built for data: Hive and Iceberg among them, each requiring a metastore, object storage, or both. A team already running those has a place to put views at no extra cost. A team not running them faces a deployment whose purpose is to hold text.

The gap is visible enough that at least one engineering team wrote and maintains a custom in-house module for exactly this, rather than adopt what was available.

### What the two environments actually need

Development and testing want view definitions handled like source: readable without a client, diffable, reviewable in a pull request, branchable, and disposable. That points at files, and file storage carries a further consequence — definitions can be synchronized into place from version control by something other than the engine, which means the store's contents can change without the engine having been told.

Production wants the opposite properties: durable across container replacement, reachable from every node, and inside the backup and access-control regime the deployment already operates. That points at a database.

### What users are asking for

Feedback comes from real deployments and is specific. Whether the security mode of a stored view should be a policy the store enforces at creation and at query time, rather than a property of whatever was handed over. Whether definitions changed underneath a running engine should become visible without a restart, and whether a lookup that misses should fall through to storage so queries keep working while cached metadata is stale, which is how standard Trino JDBC connectors already behave. Whether one deployment can hold several isolated collections of views, one per tenant, each mapping its own sources and configuration.

Nobody has established how many views one store is expected to hold.

---

## 3. Goals

- A team can store views before choosing a database, and keep storing them there afterward if nothing better is needed.
- View definitions can be treated as source code: readable, diffable, reviewable and branchable.
- A production deployment can hold views somewhere durable, shared across nodes, and already covered by existing backups.
- Views stored this way are indistinguishable from ordinary Trino views to everything downstream.
- Adopting this adds nothing to what a deployment has to operate.

---

## 4. What Is Not In Scope

- **Tables.** Views only. There is no data storage.
- **Materialized views.** They require materialized data, which is a different problem with existing solutions.
- **Being a metastore.** No table metadata, no statistics, no catalog services.
- **Compatibility across Trino releases.** The plugin interface does not offer it, so nothing here can.

---

## 5. Open Questions

- Whether a view store is expected to enforce policy on the views it holds, or only to hold faithfully what it was given. The security-mode request is the concrete instance, and the answer decides whether this is storage or governance.
- Whether the store must tolerate its contents changing from outside the engine. One real workflow says yes, and admitting it costs the guarantee that what the engine believes and what storage holds are the same thing.
- Whether isolation between multiple collections of views in one deployment is a requirement, and whether tenancy is the right frame for it.
- How many views one store should be expected to hold, which nothing has measured and which determines whether holding everything in memory has a ceiling worth documenting.
