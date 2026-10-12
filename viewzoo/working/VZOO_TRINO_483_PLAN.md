# Trino 483: Implementation Plan

## Objective

Upgrade ViewZoo from Trino 479 to Trino 483 on a new `v483` branch, cut from `v479` and changed only by a reviewed PR from the work branch `trino-483`. `v479` itself is never changed. No functional changes.

## Context

See `VZOO_TRINO_483_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `pom.xml` — project version `483`; `trino-spi`, `trino-main`, `trino-jdbc` and `trino-testing` to `483`; Airlift to `439`; Slice to `2.8`, `jackson-annotations` to `2.22` and OpenTelemetry to `1.64.0`, matching what Trino 483 supplies at runtime; the PostgreSQL driver to the current release (`42.7.14` today).
- `README.md` — `blob/v479` badge links, "Trino 479" dependency, download and `TRINO_HOME` steps, the `target/viewzoo-479` install path, and the "only been tested with Trino 479" caution.
- `CLAUDE.md` — the `target/viewzoo-479` install path.
- `src/test/docker/docker-compose.yml` — `trinodb/trino:483` image and the `viewzoo-483` plugin mount.
- `TestViewZooIntegration.java` — the `target/viewzoo-483` plugin path.
- Any source changes the compiler demands from the 480–483 SPI changes.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ViewZooMetadata.getColumnMetadata` | Returns `null`; `ColumnMetadata.comment` is now `Optional` | None expected, since ViewZoo never builds a `ColumnMetadata` |
| Integration tests | Run against the 483 image | Behavior changes in Trino surface here |
| Work items `TEST_VIEW_RENAMING`, `PG_REFRESH`, `WHY_VIEWZOO`, `SECURITY_GUIDE`, `RELEASE_BINARIES`, `MULTIPLE_ZOOS` | Blocked by this item; all target `v483` | None until they start |
| GitHub default branch | Stays `v479` after merge; switches only once `483a` is published | Visitors see `v479` and its README until then |

## Testing approach

`mvn clean package` with unit tests, then `mvn test -Pintegration` against the Trino 483 container. Both storage modes must pass as they do on `v479`. Installing into a real Trino 483 and exercising both modes by hand goes in `VZOO_TRINO_483_TESTING.md`.

## Implementation sequence

1. Cut `v483` from `v479` and push it.
2. On `trino-483`, bump the pom and fix any compile errors.
3. Update docker-compose, the integration test path, the README and `CLAUDE.md`.
4. Run unit and integration tests, then open the PR into `v483`.

## Scope boundary — what this does NOT include

- Any feature or fix, including the six items waiting on this one.
- Branches for Trino 480–482.
- Releasing a binary, which is `VZOO_RELEASE_BINARIES`.

## Open issues

None. `v479` gets no tag: the unchanged branch is the reference, and a release tag would need the release workflow added to it.
