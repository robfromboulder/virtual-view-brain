# Trino 479 Update: Implementation Plan

## Objective

Branch ViewMapper for Trino 479 and update to JDK 25. Bump dependencies, fix any breaking changes, and confirm the full test suite passes. Also establish "Branching and Versioning" instructions in the ViewMapper repo's `CLAUDE.md`, following the same model ViewZoo uses — both repos will share a branching schedule keyed to Trino version numbers. No new features.

## Context

See `VMR_TRINO_479_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning unit:
- `VMR_SCOPE.md` — problem space this fits into
- `VMR_FINDINGS.md` — relevant prior decisions
- `VMR_APPROACH.md` — design constraints

## What changes

Dependency versions in the ViewMapper project repo (`../viewmapper`) — Trino to 479, JDK to 25. Fill in specific files and any code fixes during implementation.

Add a "Branching and Versioning" section to the ViewMapper repo's `CLAUDE.md`, documenting the version-branch model: one branch per Trino version (e.g. `v479`), new branches created from the previous version branch, version branches are primary (not main), PRs target the version branch. Mirror the conventions already established in ViewZoo's `CLAUDE.md` — both repos share the same branching schedule, and each may work with later Trino versions than the branch number suggests, but are built off the same base version.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| Trino parser (Agent) | API changes in Trino 479 may require parser updates | Medium |
| JDBC connectivity (Agent) | Driver compatibility with Trino 479 | Low |
| MCP server | Subprocess wrapper — affected only if build/runtime changes | Low |
| Build configuration | POM/Gradle version properties | Low |

## Testing approach

Automated: full rebuild and existing test suite must pass across agent and MCP server modules. Manual steps (agent CLI, MCP server against new versions) live in `VMR_TRINO_479_TESTING.md`.

## Implementation sequence

1. Create branch `v479` off `main` (ViewMapper's first version branch — matches ViewZoo's naming convention)
2. Bump Trino dependency to 479
3. Bump JDK to 25
4. Fix any compilation or test failures
5. Run the full test suite
6. Add "Branching and Versioning" section to ViewMapper's `CLAUDE.md`

## Scope boundary — what this does NOT include

- New features or capabilities
- Changes unrelated to the Trino 479 / JDK 25 version bump
- Upstream Trino contributions

## Open issues

1. Extent of breaking API changes in Trino 479 — discover during implementation