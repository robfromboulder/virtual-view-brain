# Trino 479 Update: Decision Record

## Problem

ViewMapper must track Trino releases to stay compatible with the catalogs it maps. Trino 479 is the current target, and the JDK should move to 25 at the same time.

## Preferred approach: Branch and bump

Create a version branch, update Trino and JDK dependencies, fix breakages, and validate with the existing test suite.

| Aspect | Detail |
|---|---|
| Trino | Update to 479 |
| JDK | Update to 25 |
| Pattern | Follows established version-bump workflow |

- **Minimal risk** — well-understood dependency bump pattern
- **Combined update** — JDK 25 and Trino 479 together avoids two separate passes through the same code

## Alternatives considered

- **Bump Trino and JDK separately** — two branches, two PRs. Rejected: unnecessary overhead for changes that are likely to interact (JDK version affects Trino build compatibility).

## What this doesn't solve

- Compatibility with future Trino releases beyond 479
- Any pre-existing test gaps unrelated to the version bump