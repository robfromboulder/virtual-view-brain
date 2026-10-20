# Multiple Zoos: Decision Record

## Problem

Issue #10 asks whether one Trino deployment can run several ViewZoo catalogs, up to one per tenant, and how many views one catalog can hold. Separate catalogs already work: each gets its own connector instance and its own in-memory views, and filesystem and JDBC catalogs can be mixed. What's missing is documentation of the one way it goes wrong. Two catalogs pointed at the same storage silently share one set of views. For filesystem storage that means the same directory. For JDBC storage the table is always named `viewzoo` and created in the first schema on the connection's search path, so catalogs on one database share it unless their search paths differ. Postgres's default search path is `"$user", public`, so two different users without schemas of their own both land in `public`. Each catalog still caches its own copy, so shared catalogs also drift apart until restarted. Nothing in the README warns about this.

A view also resolves unqualified table names against the catalog and schema of the session that created it, which surprises anyone treating a catalog as a tenant's own space. Nobody has measured how many views one catalog can hold.

## Preferred approach: document isolation, test it, measure scale

Each catalog gets its own storage: its own directory, or its own Postgres schema chosen with the driver's `currentSchema` URL parameter (`jdbc:postgresql://host/db?currentSchema=tenant_a`), which sets the connection's search path. ViewZoo creates and uses its `viewzoo` table in that schema, with no code change. The schema must already exist, and the catalog's database user needs `CREATE` on it, because ViewZoo runs `CREATE TABLE IF NOT EXISTS` at every startup.

| Aspect | Detail |
|---|---|
| Isolation | One directory, or one Postgres schema, per catalog; sharing storage merges catalogs |
| Tenancy pattern | A catalog per tenant, granted through Trino access control; a Postgres user per tenant with rights on its own schema only; fully qualified table names inside views |
| Code | None |
| Tests | A second JDBC catalog on its own schema, proving views don't cross catalogs |
| Scale | A one-off measurement of startup and listing time at a few thousand views, recorded in the README |

- **Postgres enforces the boundary** — with a schema and user per tenant, one catalog's credentials can't read or write another tenant's views, which a table-name option alone wouldn't give.
- **Minimal change** — no code; documentation and tests only.

## Alternatives considered

- **A `viewzoo.jdbc_table` (and schema) configuration property** — what #10 first proposed. It works, but `currentSchema` already gives the same separation, and per-schema grants give stronger isolation. It stays available if someone needs two catalogs in one schema.
- **Make `listSchemaNames` return each schema once** — it currently returns a schema once per view, but Trino de-duplicates schema names before showing them, so nothing a user sees changes. Not worth a code change here.
- **Refuse to start when another catalog uses the same storage** — catches the mistake, but catalogs in separate Trino clusters can't see each other, and sharing storage on purpose is legitimate.
- **A per-user private sandbox schema** (from the #10 discussion) — a different problem, private drafts rather than tenancy, with open questions about cross-references, security mode and refresh. Declined (Rob, 2026-10-19): routing storage by session user is authorization inside storage, against the store holding what it is given; the README shows the sandbox built from per-user schemas and Trino access control, or a local filesystem catalog.

## What this doesn't solve

- Catalogs that share storage on purpose still drift apart until restarted, until refresh exists.
- A Postgres schema must exist, with `CREATE` granted to the catalog's user, before the catalog starts; ViewZoo doesn't create it.
- The scale number is a single measurement on one machine, not a guarantee.
