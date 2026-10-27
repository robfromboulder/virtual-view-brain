# ViewZoo: Scoping Statement

> V7, 2026-10-27.

This document defines the problem that ViewZoo addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states one part of the problem the ecosystem's scoping statement defines: the part where view definitions need somewhere to live.

---

## 1. Problem Statement

A view definition has to be persisted somewhere, and Trino's answer is to store it in a connector that also stores data. That is fine when the data already lives in one, and awkward in the cases that matter most here. A view backed entirely by static values has no data source to be stored beside. A team prototyping has not chosen a database yet, and picking one to hold views is the commitment the pattern was supposed to defer. A team that wants views under version control finds them locked inside a metastore instead.

The available options are heavier than the need. A Hive-compatible metastore, or an object store plus a table format, is infrastructure to deploy, secure, back up and upgrade — for what is, in the end, a small pile of SQL text. The gap is a place to keep view definitions that costs nothing to run and can be adopted before anything else has been decided.

Storage is not one problem, though, because the workflows differ. A team handling view definitions as code wants files it can read, diff, review and sync from version control. A team handling them as shared data wants something that survives container replacement, is shared across nodes, and lands in the backups that already exist. Neither workflow belongs to one environment: production deployments run both. Serving one of those well and the other badly leaves the pattern half-supported.

One of the ecosystem's design choices is given here: this obstacle has its own project.

---

## 2. State of the Problem

### What is available to store views in

The connectors that can hold views durably are the ones built for data, Hive and Iceberg among them. As of Trino 484, the Iceberg connector holds views in a REST catalog under the Iceberg view specification; Nessie and Snowflake catalogs hold none, and the documentation leaves view support in the other catalog types unstated. Every Iceberg catalog needs object storage or a shared file system mounted on every node, plus a catalog service: a Hive metastore, Glue, a REST server, or a JDBC catalog whose tables live in a database such as PostgreSQL. The memory connector holds views but loses them on restart. The PostgreSQL connector cannot create Trino views at all, and a native Postgres view is written in Postgres SQL, reads only Postgres tables, and follows Postgres permissions. A team already running those has a place to put views at no extra cost. A team not running them faces a deployment whose purpose is to hold text.

The gap is visible enough that at least one engineering team wrote and maintains a custom in-house module for exactly this, rather than adopt what was available.

### What Trino requires of a view store

Views live in catalogs, and a catalog is a connector. Any connector holding views must implement the metadata operations Trino calls to create, replace, drop, list and read them, and must persist what Trino hands it faithfully enough that the view comes back unchanged. The connector interface is where this is decided; there is no view storage outside it.

### What the two workflows actually need

Definitions handled as code want what source gets: readable without a client, diffable, reviewable in a pull request, branchable, and disposable. That points at files, and file storage carries a further consequence — definitions can be synchronized into place from version control by something other than the engine, which means the store's contents can change without the engine having been told.

Definitions handled as shared data want the opposite properties: durable across container replacement, reachable from every node, and inside the backup and access-control regime the deployment already operates. That points at a database.

### What deployments ask of a store

Feedback from real deployments names further needs. Who decides a stored view's security mode: whatever created the view, or a policy the store holds. Definitions changed outside the engine becoming visible without a restart, and queries that keep working while what the engine holds is stale. Several isolated collections of views in one deployment, one per tenant, each with its own sources and configuration.

---

## 3. Goals

- A team can store views before choosing a database, and keep storing them there afterward if nothing better is needed.
- View definitions can be treated as source code: readable, diffable, reviewable and branchable.
- A deployment can hold views somewhere durable, shared across nodes, and already covered by existing backups.
- Views stored this way are indistinguishable from ordinary Trino views to everything downstream.
- Storing views adds nothing to what a deployment has to operate.

---

## 4. What Is Not In Scope

- **Tables.** Views only. There is no data storage.
- **Materialized views.** They require materialized data, which is a different problem with existing solutions.
- **Being a metastore.** No table metadata, no statistics, no catalog services.

---

## 5. Open Questions

- Whether a view store is expected to enforce policy on the views it holds, or only to hold faithfully what it was given. The security-mode request is the concrete instance, and the answer decides whether this is storage or governance.
- Whether the store must tolerate its contents changing from outside the engine. One real workflow says yes.
- Whether isolation between multiple collections of views in one deployment is a requirement, and whether tenancy is the right frame for it.
- How many views one store should be expected to hold, which nothing has measured.
