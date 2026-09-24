# Test View Renaming: Implementation Plan

## Objective

Add `ALTER VIEW ... RENAME TO` test cases to ViewZoo's test suite, covering the renaming variations that the current suite omits. Purely additive — no production code changes.

## Context

See `VZOO_TEST_VIEW_RENAMING_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

Test files in the ViewZoo project repo (`../viewzoo`). Fill in specific files and cases during implementation.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| Existing test suite | New test cases follow established patterns | Low — additive only |

## Testing approach

The work item is itself test work. Automated: the new test cases must pass in the existing suite. No manual testing beyond running the suite. Manual steps live in `VZOO_TEST_VIEW_RENAMING_TESTING.md`.

## Implementation sequence

1. Identify existing test patterns for DDL operations in the ViewZoo test suite
2. Add `ALTER VIEW x RENAME TO y` test case variations
3. Run the full test suite to confirm new tests pass and no regressions

## Scope boundary — what this does NOT include

- Other DDL operation test cases (DROP, CREATE, ALTER beyond rename)
- Production code changes
- Test infrastructure changes

## Open issues

1. Exact rename variations to cover (simple rename, rename across schemas, rename with dependencies) — decide during implementation based on what the codebase supports