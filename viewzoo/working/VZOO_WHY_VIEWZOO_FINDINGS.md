# Why ViewZoo: Decision Record

## Problem

The README never says why someone would choose ViewZoo over the alternatives a reader already knows, and the mini-brain doesn't either. The most common confusion is with Trino's PostgreSQL connector. That connector cannot create views at all: its SQL support covers tables and schemas only. Native Postgres views are written in Postgres SQL, see only Postgres tables, and follow Postgres permissions. A ViewZoo view is Trino SQL that can join any catalog, and its security mode belongs to Trino. Among the real alternatives for storing Trino views (Hive metastore, Glue, the Iceberg REST and JDBC catalogs), ViewZoo's JDBC mode is the only one needing no metastore and no warehouse — just one Postgres table. The Iceberg JDBC catalog is the nearest, and it still requires `iceberg.jdbc-catalog.default-warehouse-dir` for its metadata files.

The README also casts the two storage modes as development and production, and recommends JDBC for "multi-container and Kubernetes deployments" without qualification. Views are loaded once at startup, so coordinators sharing a table drift apart until restarted. The production claim is stronger than the code supports.

## Preferred approach: positioning in the README and the mini-brain, refresh stated honestly

A documentation-only change. The README gains a short "Why ViewZoo?" section near the top, recasts the two storage modes as two workflows, shows a PG connector catalog working alongside ViewZoo, and states plainly that views load at startup. The mini-brain gains the same positioning at closeout.

| Aspect | Detail |
|---|---|
| Core sentence | "ViewZoo isn't a replacement for the PostgreSQL connector: it uses Postgres to store Trino views, which can query any catalog." |
| Comparison | Memory connector (doesn't persist), PG connector (no Trino views), Hive metastore and Glue (a metastore to run), Iceberg JDBC and REST catalogs (need a warehouse), ViewZoo filesystem, ViewZoo JDBC |
| Two workflows | Filesystem: view definitions as code, with git and PR review. Postgres: shared, durable views with backups and SQL access to the definitions |
| Working together | A PG connector catalog over the same database makes `select * from pg.public.viewzoo` a queryable list of the views |
| Refresh | Both modes load views at startup; a restart picks up changes made outside the connector |

- **Ships independently** — no code dependency, so the positioning lands long before live refresh.
- **Honest now, upgradable later** — the refresh statement is one sentence that the live-refresh work changes when it merges.
- **Matches real use** — the user who filed #13 and #14 runs git-synced filesystem views in production (stated in #10 and #14), treating the filesystem mode as definitions-as-code rather than a development shortcut.

## Alternatives considered

- **Ship the positioning with live refresh** — the original single item. Rejected because the docs are ready long before the code, and coupling them holds back the cheaper change.
- **Drop the multi-container recommendation entirely until refresh lands** — accurate but undersells JDBC mode, which already gives durability, backups and a shared store. Qualifying the claim is enough.

## What this doesn't solve

- Coordinators sharing a Postgres table still drift until restarted; only the docs say so.
- The comparison is a snapshot of other projects' capabilities and will age as they change.

## Reversals

- `VZOO_APPROACH.md`, Strategic Approach — its framing of files as the development backend and the database as the production backend. Both are recast as workflows, neither tied to an environment.
