# Security Guide: Decision Record

## Problem

ViewZoo has no security guide, so an operator deciding whether to run it has to infer its security properties from the code (issue #11). Three things matter and none is written down. Views keep whichever security mode they were created with, `DEFINER` or `INVOKER`, and the connector stores that mode without enforcing any policy on it. View definitions have no overall length check and are all held in memory, so a large or numerous set of definitions is a resource risk; a definition whose SQL exceeds Jackson's 20,000,000-character string limit is written but skipped at the next startup. Storage is read only when Trino starts, and anyone who can write it can change views, including the owner a `DEFINER` view runs as; a file or row that fails to parse is skipped with a warning. The repository also has no vulnerability-reporting policy: private vulnerability reporting and Dependabot alerts are off, and code scanning is not configured. Secret scanning and push protection are already on.

## Preferred approach: a SECURITY.md that documents current behavior

A `SECURITY.md` at the repository root, in GitHub's conventional form, so it appears in the repository's Security tab. It states how to report a vulnerability, then documents the connector's security properties as they are today. Turning on Dependabot alerts and code scanning is a repository-settings task in the burndown, not text in the guide.

| Aspect | Detail |
|---|---|
| Location | Repository root on `v483`; GitHub's Security tab reads the default branch, so it shows there once `v483` becomes the default at the `483a` release |
| Reporting | How to report privately (GitHub private vulnerability reporting); only the newest version branch receives fixes |
| Security modes | Both `DEFINER` and `INVOKER` are stored and returned unchanged; the connector enforces no policy on them |
| Resource limits | Names are capped at 100 characters, but a definition's length is not, every definition is held in memory, and SQL over 20,000,000 characters is skipped at the next startup |
| Filesystem storage | Trino needs read and write access to `viewzoo.dir`; anyone with write access can add, change or remove views at the next restart; names resolving outside the directory are rejected |
| JDBC storage | The JDBC user needs to create, read and write the `viewzoo` table; anyone with write access to that table can change views at the next restart; keep the password out of plain-text catalog files using Trino's secret substitution |

- **Documents, doesn't change** — the guide describes the code as it is, so it can ship now and change as features land.
- **Write access is the real boundary** — whoever can write the storage can change what every query through a `DEFINER` view runs as, which is the most important thing for an operator to know.

## Alternatives considered

- **Add a definition length check in the same item** — closes the gap instead of documenting it, but it is a code change with its own limit to choose, and it would hold back the guide. It can become its own work item.
- **Put the security material in the README** — rejected because GitHub surfaces `SECURITY.md` specifically, and the README is already being reworked by another item.

## What this doesn't solve

- The missing length check remains; only the guide mentions it.
- Policy on security modes stays unenforced until the `VZOO_SECURITY_MODE` work item lands.
- The guide has to be carried forward to each new version branch, and updated when the default branch changes.
