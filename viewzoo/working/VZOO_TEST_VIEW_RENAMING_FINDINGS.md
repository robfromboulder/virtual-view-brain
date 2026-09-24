# Test View Renaming: Decision Record

## Problem

ViewZoo's test cases don't include `ALTER VIEW x RENAME TO y` variations. View renaming is a standard DDL operation that could regress undetected without coverage.

## Preferred approach: Add rename test cases to the existing suite

Follow the existing test patterns in the ViewZoo test suite and add rename-specific cases. No new test infrastructure or production code changes required.

| Aspect | Detail |
|---|---|
| Scope | `ALTER VIEW ... RENAME TO` variations only |
| Pattern | Follow existing DDL test conventions in the suite |
| Risk | Low — purely additive |

- **Simplicity** — uses established test patterns, no new abstractions
- **Coverage** — fills a specific documented gap (GitHub issue viewzoo#9)

## Alternatives considered

- **Broader DDL test sweep** — cover all missing DDL operations at once. Rejected: scope creep for a single-issue fix; other DDL gaps can be separate work items.

## What this doesn't solve

- Test coverage for other DDL operations beyond rename
- Any behavioral issues with rename itself (this item only adds tests, not fixes)