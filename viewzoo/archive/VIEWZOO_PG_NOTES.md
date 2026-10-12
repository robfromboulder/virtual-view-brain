# ViewZoo + PostgreSQL: Value Analysis

Written 2026-10-05. Based on the `v479` branch and the open GitHub issues.

## Short answer

ViewZoo doesn't compete with Trino's PostgreSQL connector, because that connector can't create views at all. ViewZoo's JDBC mode uses Postgres only as a place to store Trino views. The PostgreSQL storage mode adds real value, but the README never says what it is, and the current code weakens the main reason to pick the JDBC mode.

## How ViewZoo differs from the PostgreSQL connector

- **No `CREATE VIEW` in the PG connector.** Its SQL support covers tables and schemas (INSERT, UPDATE, DELETE, MERGE, CREATE/DROP TABLE and SCHEMA). It has no view management.
- **Native Postgres views can only use Postgres tables.** You can create a view inside Postgres and Trino will read it, but it's written in Postgres SQL and can't reach other catalogs. A ViewZoo view is written in Trino SQL, so one view can join Iceberg, Kafka, MySQL and `system.runtime` together.
- **The view's security mode belongs to Trino.** With `SECURITY DEFINER`, users can query a view across catalogs without having access to the underlying tables. Postgres views follow Postgres permissions, which know nothing about other catalogs.

The real alternatives for storing Trino views are a Hive metastore, Glue, the Iceberg REST catalog, and the Iceberg JDBC catalog. The Iceberg JDBC catalog is the closest one: it keeps its catalog in Postgres and supports views. But it requires `iceberg.jdbc-catalog.default-warehouse-dir`, so you still need a filesystem or object storage for its metadata files. ViewZoo's JDBC mode is the only option here with no metastore, no warehouse, and just one Postgres table. That's the selling point, and the README doesn't say it.

## The current code undercuts the "production / multi-container" claim

The README recommends JDBC storage for "multi-container and Kubernetes deployments," but:

- **Views are loaded once at startup** (the `ViewZooMetadata` constructor calls `storageClient.getViews()`). If two coordinators or two clusters share the same Postgres table, they drift apart until restarted. A row written straight into the table (for example by a GitOps sync job) isn't seen either. This is issue #14, and it matters more for JDBC than for the filesystem mode.
- **Smaller problems:**
  - `listSchemaNames` returns duplicate schema names, because there's no `distinct`.
  - `createView` updates the in-memory map before the storage write, so a failed write leaves the cache claiming the view exists.
  - A new connection is opened through `DriverManager` for every operation, with no pool.
  - The table name `viewzoo` is hard-coded into whatever schema the JDBC user lands in.
  - The startup error message is missing a ": " separator.

## Suggested changes to the documentation

1. **Add a short "Why ViewZoo?" section near the top**, with a table comparing the memory connector (doesn't persist), the PG connector (no Trino views), Hive metastore/Glue, the Iceberg JDBC/REST catalogs (need a warehouse), and ViewZoo's two modes. Answer the core question in one sentence: *"ViewZoo isn't a replacement for the PostgreSQL connector: it uses Postgres to store Trino views, which can query any catalog."*
2. **Present the two storage modes as two workflows**, not a dev mode and a production mode:
   - Filesystem: view definitions as code (git, PR review). This matches what the user in #10, #13 and #14 is already doing.
   - Postgres: shared, durable views for many coordinators, with backups and SQL access to the definitions.
3. **Document how the two connectors work together.** Add a PG connector catalog pointed at the same database, and `select * from pg.public.viewzoo` becomes a queryable list of your views. Nobody else offers that.
4. **Be honest about refresh until it's fixed.** State that views are loaded at startup, rather than claiming multi-coordinator suitability without qualification.

## New capabilities that only Postgres makes easy

Ordered by value:

1. **Cross-coordinator refresh using `LISTEN/NOTIFY`.** On every write, send `NOTIFY viewzoo`, and have each coordinator listen and reload. This fixes #14 for JDBC with instant updates and no timer, and makes the multi-container claim true. A timer or a reload function (as discussed in #14) can stay as the filesystem-mode fallback.
2. **Store definitions as `jsonb` and add metadata columns** (`created_at`, `updated_at`, `created_by` from the session user). Then the view catalog itself can be queried and audited, for example "which views reference `iceberg.sales`?" or "who changed this last?". That also helps the lineage work moved to viewmapper (#6).
3. **History table using a trigger.** Every replace or drop keeps the previous definition, which gives the Postgres mode the same revision history git gives the filesystem mode, plus a way to roll back.
4. **Multi-tenancy (#10):** add a `tenant` column, or map a `sandbox` schema to a per-user key. Postgres row-level security can then enforce it at the database too, which is much simpler than per-user folders.
5. **Config options for the database location:** `viewzoo.jdbc_schema` / `jdbc_table`, plus a connection pool. These let several Trino clusters (prod and staging) share one Postgres safely.
6. **Security-mode enforcement (#13)** works in either storage mode. Postgres can also back it with a `CHECK` constraint, so out-of-band writes can't sneak in `DEFINER` views.

## Recommended first step

Do item 1 of the new capabilities (`LISTEN/NOTIFY` refresh) together with the "Why ViewZoo?" section. The refresh fix makes the production claim true, and the doc section explains why someone would choose ViewZoo.
