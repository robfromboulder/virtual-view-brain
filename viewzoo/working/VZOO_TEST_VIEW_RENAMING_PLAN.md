# Test View Renaming: Implementation Plan

## Objective

Implement `ALTER VIEW ... RENAME TO` in ViewZoo (previously unsupported) and cover it with integration tests on both storage backends.

## Context

See `VZOO_TEST_VIEW_RENAMING_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `ViewZooMetadata` — `renameView` override; name validation extracted to a shared helper
- `ViewZooStorageClient` — new `renameView` method, implemented by `ViewZooJdbcClient` and `ViewZooLocalFileSystemClient`
- `TestViewZooIntegration` — `testViewRenaming` plus two assertion helpers

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| Existing test suite | New test cases follow established patterns | Low — additive only |
| `createView` | Validation moved into `validateName`, behavior unchanged | Low — covered by existing name tests |

## Testing approach

Automated: `testViewRenaming` must pass on both catalogs alongside the existing integration tests. No manual testing beyond running the suite. Manual steps live in `VZOO_TEST_VIEW_RENAMING_TESTING.md`.

## Implementation sequence

1. Add `renameView` to the storage interface and both clients
2. Override `renameView` in `ViewZooMetadata`
3. Add `testViewRenaming` to the integration suite
4. Run the full integration suite on both catalogs

## Scope boundary — what this does NOT include

- Other DDL operation test cases (DROP, CREATE, ALTER beyond rename)
- Test infrastructure changes

## Open issues

None. Variations covered: in-schema, cross-schema, existing target, missing source, invalid target, restart persistence. Cross-catalog rename is rejected by the Trino engine before reaching the connector.