# Why ViewZoo: Implementation Plan

## Objective

Explain in the README why ViewZoo exists relative to Trino's PostgreSQL connector and the other places Trino views can live, recast the two storage modes as two workflows, and state refresh behavior honestly. Fold the same positioning into the ViewZoo mini-brain at closeout. Targets the `v483` branch. No code changes.

## Context

See `VZOO_WHY_VIEWZOO_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `README.md`:
  - add a "Why ViewZoo?" section near the top, with the core sentence and the comparison table, and add it to the table of contents.
  - rewrite the intros to "Running With Filesystem Storage" and "Running With JDBC Storage" as the two workflows. Recast the filesystem tip, which calls the mode "particularly valuable for development environments". Replace "preferred for multi-container and Kubernetes deployments, and production environments in general" with what JDBC mode actually gives.
  - add a short section on pairing ViewZoo with a PG connector catalog over the same database, with an example catalog file and query.
  - add to "Limitations": views are loaded at startup, so changes made outside the connector, or by another coordinator, need a restart.
- Mini-brain, at closeout: the reversals in `VZOO_WHY_VIEWZOO_FINDINGS.md`.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `VZOO_PG_REFRESH` work item | Its README edit rewrites the refresh limitation added here | Whichever merges second rebases its README edit onto the other |
| Other version branches | The README differs per branch | The change lands on `v483` and is carried forward like code |

## Testing approach

No automated tests change, and none run beyond confirming the build is unaffected. Manual checks are in `VZOO_WHY_VIEWZOO_TESTING.md`: the README renders on GitHub, anchors resolve, and the PG connector example works against the docker-compose stack.

## Implementation sequence

1. "Why ViewZoo?" section and comparison table.
2. Workflow framing of the two storage sections.
3. PG connector pairing example, verified against the docker-compose stack.
4. Refresh limitation.

## Scope boundary — what this does NOT include

- Any code change, including live refresh (`VZOO_PG_REFRESH`) and the small JDBC fixes.
- Docs for features that don't exist yet: metadata columns, history, multi-tenancy, security-mode enforcement.

## Open issues

1. Whether the PG connector example should also ship as a catalog file in `src/test/docker`. `VZOO_PG_REFRESH` adds one for its tests, and this item could add it first.
2. How much detail the comparison table carries per alternative before it becomes a maintenance burden.
3. The comparison's claims about other connectors come from the PG notes and must be checked against the Trino 483 docs: the PostgreSQL connector's lack of view support, and the Iceberg JDBC catalog's view support and warehouse requirement.
