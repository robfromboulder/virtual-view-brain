# Trino 483: Decision Record

## Problem

ViewMapper is built against Trino 479: the agent's SQL parser and JDBC driver are both pinned to it, and the released image is `479a`. Trino has since released 480 through 483, so ViewMapper can't parse syntax added since 479 and ships an older driver.

ViewMapper also has no stable place for what users run today. All work happens on `main`, which has already moved five commits past the `v479a` tag. Users pin a released image tag in their Claude Desktop config and keep it for months, so the source behind that tag should stay easy to find and never change.

## Preferred approach: adopt version branches, then upgrade on `v483` by PR

Adopt ViewZoo's branching convention. Cut `v479` from the tip of `main` and leave it unchanged as the stable reference for current users. Cut `v483` from `v479`, do the upgrade on a work branch `trino-483`, and merge it into `v483` by PR. `main` stops receiving changes.

| Aspect | Detail |
|---|---|
| Branches | `v479` frozen at today's `main`; `v483` for the upgrade and all further work; `main` unused |
| Default branch | `v479` as soon as it's cut (identical to `main`, so nothing visible changes); `v483` once `483a` is released |
| Java | Unchanged: Trino 483 still targets Java 25 |
| Dependencies | `trino-parser` and `trino-jdbc` 479 → 483, through the `trino.version` property |
| Parser | `DependencyExtractor` builds on Trino's `DefaultTraversalVisitor`, which in 483 descends into new relations such as `PIVOT`, so tables inside new syntax are still found |
| Version strings | Agent pom version and the CLI's `--version` string in `Main.java`; MCP server `pyproject.toml` version and Dockerfile JAR name; `build.sh`, `clean.sh`, and `release.sh`, which accepts only `479[a-z]`; docs across the root, agent and MCP server directories; the README hero's revision number |
| Release | After merge, `./release.sh 483a` publishes image `483a` and git tag `483a`. `release.sh` stops adding a `v` prefix, so tags match ViewZoo's and can't be mistaken for the `v483` branch; the published `v478a`–`v479a` tags stay |

- **Same convention across the ecosystem** — both tools branch per Trino version and tag releases as the version plus a letter, so a contributor learns one model.
- **A frozen reference** — `v479` holds exactly what `479a` users run, plus the docs since, and never changes.
- **Reviewed** — the upgrade gets a PR and a test run before it becomes the base for other work.

## Alternatives considered

- **Upgrade in place on `main`** — ViewMapper's current model, and the least work. But `main` then no longer matches what `479a` users run, and the next upgrade repeats the problem.
- **Keep working on `main` but tag `v479` as the reference** — a tag preserves the code, but contributions and fixes for 479 would have nowhere to land.

## What this doesn't solve

- Users on Trino 480–482 still have no matching build.
- Fixes on `v483` aren't carried back to `v479`.

## Reversals

- `VMR_APPROACH.md` has no branching decision yet, so adopting version branches is an addition. But this item gives ViewMapper the branching convention `VZOO_APPROACH.md` records for ViewZoo, and ViewZoo is adopting the release-tag convention `VMR_APPROACH.md` records for ViewMapper. A convention shared by both lobes belongs in the hub, so closeout should place it in `VV_APPROACH.md`. The two lobes' copies then reduce to naming it.
