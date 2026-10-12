# Security Guide: Implementation Plan

## Objective

Add a `SECURITY.md` that tells users how to report a vulnerability and documents ViewZoo's security properties as they are today: security modes, unbounded definition length, and who can change views in each storage mode. Turn on Dependabot alerts and code scanning for the repository. Targets the `v483` branch. No code changes.

## Context

See `VZOO_SECURITY_GUIDE_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `SECURITY.md` (new, repository root):
  - reporting a vulnerability, and which version branches are supported.
  - security modes: both are supported, stored and returned unchanged, and not enforced.
  - resource limits: no overall length check on definitions, all held in memory.
  - filesystem storage: required permissions, that write access to the directory means control of the views, and that a malformed file stops the catalog from loading.
  - JDBC storage: required database privileges, that write access to the table means control of the views, that a malformed row stops the catalog from loading, and keeping the password out of catalog files.
- `README.md` — link to `SECURITY.md`.
- Repository settings (no commit): turn on Dependabot alerts, private vulnerability reporting, and code scanning default setup.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `VZOO_WHY_VIEWZOO` work item | Both edit the README | Whichever merges second rebases its README edit onto the other |
| `VZOO_PG_REFRESH` work item | Adds privileges the JDBC user needs (creating a function and a trigger) | The guide's JDBC section must be updated when it merges |
| Issue #13 | Would make the connector enforce a security-mode policy | The guide's security-mode section must be updated if it lands |

## Testing approach

No automated tests change. Manual checks are in `VZOO_SECURITY_GUIDE_TESTING.md`: the guide appears in the repository's Security tab, its claims match the code on `v483`, and the settings are on.

## Implementation sequence

1. Turn on private vulnerability reporting, so the guide can point to it.
2. Write `SECURITY.md` and link it from the README.
3. Turn on Dependabot alerts and code scanning, and triage anything they report.

## Scope boundary — what this does NOT include

- A length check on view definitions, or any other code change.
- Enforcing a security-mode policy (#13).
- A threat model or security review of Trino itself.

## Open issues

1. Which version branches the guide calls supported: only the latest, or the latest few.
2. Whether to also turn on Dependabot security updates, which open PRs automatically against the default branch.
3. Whether a definition is truly unbounded. Storage uses a plain Jackson `ObjectMapper`, whose default read constraints cap a single string's length. If they do, a definition over the cap can be written but fails to load at the next startup, which stops the catalog. Confirm the Jackson version and the behavior before the guide describes it.
4. Whether a quoted view or schema name containing `/` can write a file outside `viewzoo.dir`. Names containing `.` are rejected, which blocks `..`, but nothing rejects `/`. Test this before the guide says anything about path safety. If it can escape the directory, it's a vulnerability to fix before publishing the guide, not something to document.
