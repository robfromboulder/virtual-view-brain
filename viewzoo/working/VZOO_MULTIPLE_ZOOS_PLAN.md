# Multiple Zoos: Implementation Plan

## Objective

Make running several ViewZoo catalogs in one deployment, up to one per tenant, documented and tested: one storage location per catalog, with Postgres schemas chosen through `currentSchema`. Measure how many views a catalog can hold. Targets the `v483` branch. No code changes and no new configuration.

## Context

See `VZOO_MULTIPLE_ZOOS_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `README.md`:
  - a "Running Multiple Catalogs" section: one directory or one Postgres schema per catalog, an example catalog file using `currentSchema`, the schema and `CREATE` grant it needs first, the warning that shared storage (including the default `public` schema) merges catalogs, and that filesystem and JDBC catalogs can be mixed.
  - the catalog-per-tenant pattern: Trino access control per catalog, a Postgres user per tenant limited to its schema, and fully qualified names inside views.
  - a per-user sandbox built from what exists: a schema per user enforced by Trino access control, or a local Trino with a filesystem catalog for drafting views before a PR.
  - under Limitations, the measured view count and startup time.
- `src/test/docker/` — a Postgres init script creating a second schema, and a `testjdbc2` catalog using `currentSchema` for it.
- `TestViewZooIntegration.java` — a test that views created in one JDBC catalog don't appear in the other.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooJdbcClient` startup `CREATE TABLE IF NOT EXISTS viewzoo` | Unqualified, so it lands in the `currentSchema` schema | Fails if that schema doesn't exist; documented, not handled |
| `VZOO_PG_REFRESH` work item | Its notification channel is a fixed `viewzoo` | With a table per schema in one database, every catalog reloads on any tenant's change; its channel should include the schema |
| `VZOO_SECURITY_GUIDE` work item | Both edit the README | Whichever merges later rebases its README edit |

## Testing approach

Integration tests against the docker-compose stack: the existing `testjdbc`/`testfs` suite stays green, plus isolation between the two JDBC catalogs. The scale measurement is a one-off by hand, recorded in `VZOO_MULTIPLE_ZOOS_TESTING.md` with the machine and numbers.

## Implementation sequence

1. Second schema and catalog in the test stack, and the isolation test.
2. README sections.
3. Scale measurement, then the Limitations note.

## Scope boundary — what this does NOT include

- A per-user sandbox schema mapped to separate storage per user (#10 discussion); declined, beyond the README paragraph above.
- A table-name configuration property.
- Refresh (#14) and security-mode enforcement (#13).

## Open issues

1. Whether the scale measurement should become an automated test later, once refresh makes reload cost matter.
