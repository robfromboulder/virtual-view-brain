# Trino 483: Decision Record

## Problem

ViewZoo is built against Trino 479, and a plugin build works with exactly one Trino release. Trino has since released 480, 481, 482 and 483, so anyone running a current Trino can't use ViewZoo without porting it themselves.

## Preferred approach: a reviewed upgrade into a new `v483` branch

Cut `v483` from the tip of `v479` unchanged, do the upgrade on a work branch `trino-483`, and merge it into `v483` by PR. Once merged, `v483` is the base for all further work. `v479` stays unchanged as the stable reference for current users and forks, and remains the default branch until the first `v483` release, `483a`, is published.

| Aspect | Detail |
|---|---|
| Java | Unchanged: Trino 483 still targets Java 25 |
| Dependencies | Trino artifacts 479 → 483; Airlift aligned with Trino 483's 439. Slice, `jackson-annotations` and OpenTelemetry are supplied by Trino at runtime, so they track Trino 483's versions (Airbase 395: Slice 2.8, Jackson 2.22, OpenTelemetry 1.64.0), not the newest releases. The PostgreSQL driver is bundled with the plugin, so it goes to the current release |
| SPI | Every method ViewZoo overrides has the same signature in 483 as in 479; `ConnectorMetadata` only gains a default method. The breaking changes from 480 to 483 are in interfaces ViewZoo doesn't implement (split managers, page sources, `Constraint`, blocks), except `ColumnMetadata.comment` becoming `Optional`, which ViewZoo never constructs |
| Tested compatibility | Trino's plugin loader has no SPI version check. The unmodified `v479` build passed all 6 integration tests (both catalogs) against `trinodb/trino:483` on 2026-10-12, with only the test image changed. The upgrade is version bumps, not compatibility fixes, and a clean first build is expected |
| Version strings | The pom version, README install steps and badges, the repo's `CLAUDE.md`, the docker-compose Trino image, and the integration test's plugin path all carry `479` |
| Skipped versions | No branches for 480–482 |

- **Reviewed** — earlier upgrades were one commit pushed straight to the new branch. A PR gives the upgrade a review and a CI run before it becomes the base for other work.
- **Upgrade first** — the other open items retarget to `v483`, so each change is made once rather than landed on `v479` and carried forward by hand.

## Alternatives considered

- **Push the upgrade straight to `v483`** — matches past practice and is quicker, but nothing reviews or tests it before other work builds on it.
- **Land the open items on `v479` first, then carry them forward** — keeps `v479` current, but every item is then done twice.
- **Branch for each of 480–482 as well** — serves users stuck on those releases, but nobody has asked, and each branch is one more to carry fixes to.

## What this doesn't solve

- Users on Trino 480–482 still have no matching build.
