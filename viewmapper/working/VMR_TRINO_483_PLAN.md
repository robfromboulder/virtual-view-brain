# Trino 483: Implementation Plan

## Objective

Move ViewMapper to version branches and upgrade it from Trino 479 to Trino 483. Cut `v479` from `main` as a frozen reference, cut `v483` from `v479`, and change `v483` only by a reviewed PR from the work branch `trino-483`. Release `483a` from `v483`. `v479` and `main` are never changed afterwards. No functional changes.

## Context

See `VMR_TRINO_483_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VMR_SCOPE.md` — problem space this fits into
- `VMR_FINDINGS.md` — relevant prior decisions
- `VMR_APPROACH.md` — design constraints

## What changes

- Repository: branches `v479` and `v483`; the default branch moves `main` → `v479` → `v483` (see Implementation sequence).
- `viewmapper-agent/pom.xml` — project version and `trino.version` to `483`; fix any compile errors in `TrinoSqlParser` or `DependencyExtractor`.
- `viewmapper-agent/.../Main.java` — the CLI's `--version` string, `ViewMapper 483`.
- `viewmapper-mcp-server/pyproject.toml` — version `483`.
- `viewmapper-mcp-server/Dockerfile` — `viewmapper-483.jar` in the `COPY` and `VIEWMAPPER_JAR`.
- `build.sh` and `clean.sh` — JAR name, image tag and summaries.
- `release.sh` — accept `483[a-z]`, and the usage example. Tag the release `483a` instead of `v483a`, matching ViewZoo and `VMR_APPROACH.md`; a `v` prefix reads like a version branch name. Existing tags `v478a`–`v479a` stay as published.
- Docs: root `README.md` (Claude Desktop examples to `483a`), `CLAUDE.md`; the agent's `README.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `TESTING.md`; the MCP server's `README.md` and `TESTING.md`. Contributor docs say that contributions target the current version branch.
- `.github/images/hero.src.svg` — revision `483` in the drawn title block and the `aria-label`, re-exported to `hero.svg` with the brain's `text2path.py`; the README's hero alt text to match.
- Tests: parser cases for syntax added in 480–483 that can carry table references, at least `PIVOT`.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `DependencyExtractor` (`DefaultTraversalVisitor`) | Its overrides of `visitTable`, `visitWith` and others run under the 483 visitor | Behavior changes in the visitor show up as missing or extra dependencies; the parser test suite catches them |
| `trino-jdbc` 483 | Connects to users' Trino servers, which may be older | Usually compatible across versions; check against an older server |
| Released image `479a` and tag `v479a` | Unchanged | None; `479a` users are unaffected |
| `main` | Frozen at the commit `v479` is cut from | Links to `main` keep working but stop updating |

## Testing approach

`mvn clean package` with the agent's unit tests, including new parser cases; `pytest` for the MCP server; `build.sh` builds the image. Checking Claude Desktop against the built image by hand, in both test-dataset and JDBC modes, goes in `VMR_TRINO_483_TESTING.md`.

## Implementation sequence

1. Cut `v479` from the tip of `main`, push it, and make it the default branch.
2. Cut `v483` from `v479` and push it.
3. On `trino-483`, bump the versions and fix any compile errors.
4. Add parser tests for new syntax.
5. Update scripts, Dockerfile, docs and the hero.
6. Run the tests and `build.sh`, then open the PR into `v483`.
7. After merge, run `./release.sh 483a`, then make `v483` the default branch.

## Scope boundary — what this does NOT include

- Any feature or fix beyond what 483 requires.
- Branches for Trino 480–482.
- A release for `v479`, which already has `479a`.

## Open issues

1. Whether `release.sh` should read the version from the pom instead of hard-coding it, so each version branch needs no edit there.
2. Whether the `v479` and `main` branches should be protected against pushes once frozen.
