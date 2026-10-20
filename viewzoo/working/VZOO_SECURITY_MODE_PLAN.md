# Security Mode: Implementation Plan

## Objective

Let an operator restrict which view security modes a catalog accepts, so a view whose `owner` storage can't vouch for can't run as that owner. A configuration property, defaulting to today's behavior of accepting both modes, makes the connector refuse to create a disallowed view and refuse to serve one found in storage. Targets the `v483` branch. Replaces GitHub issue #13.

## Context

See `VZOO_SECURITY_MODE_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `config/` — a property (name and values to settle, e.g. `viewzoo.allowed_security_mode=any|invoker`), default `any`.
- `ViewZooMetadata.java`
  - `createView`: refuse a view whose mode isn't allowed, before storage is written.
  - Views found in storage with a disallowed mode: handled per the open issue below.
- `README.md` — document the property and the threat it addresses.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `ConnectorViewDefinition.isRunAsInvoker()` / `getOwner()` | The mode is read from Trino's own definition | None expected; verify how Trino sets owner for `INVOKER` views |
| `getView` / `getViews` in `ViewZooMetadata` | Where a stored disallowed view would be refused or hidden | Behavior must be consistent between listing, `information_schema` and query |
| `VZOO_STORAGE_ERRORS` work item | Same principle: one bad entry doesn't affect the rest | A disallowed view must not fail the whole load |
| `VZOO_FS_REFRESH` / `VZOO_PG_REFRESH` work items | Reloaded views pass through the same check | The check belongs where every load path goes through it |
| `VZOO_SECURITY_GUIDE` work item | Documents security modes as unenforced | Its security-mode section must be updated if this lands first |

## Testing approach

Unit, in `TestViewZooMetadata`: with the policy set, creating a `DEFINER` view fails and storage is untouched; an `INVOKER` view succeeds; with the default, both succeed. A disallowed definition supplied by the fake storage client is handled as decided. Integration: a catalog with the policy set, a `DEFINER` view file or row placed in storage behind the connector's back, and the resulting behavior through SQL.

## Implementation sequence

1. Check whether Trino can already forbid `DEFINER` views across all catalogs; if it can, reduce this item to documentation.
2. Config property and the create-time check.
3. Load- or query-time handling.
4. Integration tests and README.

## Scope boundary — what this does NOT include

- Rewriting a disallowed view to another mode.
- Policy on anything else in a definition (SQL text, referenced catalogs, owner names).
- Authenticating who wrote a file or row.

## Open issues

1. How a disallowed view found in storage behaves: fail when queried with a clear error, so a user without log access can see why (the #13 requester's preference), or skip and log on load, as `VZOO_STORAGE_ERRORS` does for bad entries.
2. Whether `DEFINER`-only is ever a useful policy, or the property is just a switch for `INVOKER`-only.
3. Whether a disallowed view should still appear in listings and `information_schema`.
4. The error code for a refused create (`PERMISSION_DENIED`, `INVALID_VIEW` or `NOT_SUPPORTED`).
