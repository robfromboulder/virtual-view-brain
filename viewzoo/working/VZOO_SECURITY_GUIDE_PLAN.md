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
  - resource limits: no overall length check on definitions, all held in memory, SQL over Jackson's 20,000,000-character string limit skipped at the next startup.
  - who can change views: storage is read only at startup, write access means control of the views and of a `DEFINER` view's owner, and invalid files or rows are skipped with a warning.
  - filesystem storage: required permissions, and that names resolving outside `viewzoo.dir` are rejected.
  - JDBC storage: required database privileges, and keeping the password out of catalog files.
- `README.md` — link to `SECURITY.md`.
- Repository settings (no commit): turn on Dependabot alerts, private vulnerability reporting, and code scanning default setup.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `VZOO_WHY_VIEWZOO` work item | Both edit the README | Whichever merges second rebases its README edit onto the other |
| `VZOO_PG_REFRESH` work item | Adds privileges the JDBC user needs (creating a function and a trigger) | The guide's JDBC section must be updated when it merges |
| `VZOO_SECURITY_MODE` work item | Would make the connector enforce a security-mode policy | The guide's security-mode section must be updated if it lands |

## Testing approach

No automated tests change. Manual checks are in `VZOO_SECURITY_GUIDE_TESTING.md`: the guide appears in the repository's Security tab once `v483` is the default branch, its claims match the code on `v483`, and the settings are on.

## Implementation sequence

1. Turn on private vulnerability reporting, so the guide can point to it.
2. Write `SECURITY.md` and link it from the README.
3. Turn on Dependabot alerts and code scanning, and triage anything they report.

## Scope boundary — what this does NOT include

- A length check on view definitions, or any other code change.
- Enforcing a security-mode policy (`VZOO_SECURITY_MODE`).
- A threat model or security review of Trino itself.

## Open issues

1. Whether to also turn on Dependabot security updates, which open PRs automatically against the default branch.
