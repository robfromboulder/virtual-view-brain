# Security Guide: Decision Record

## Problem

ViewZoo has no security guide, so an operator deciding whether to run it has to infer its security properties from the code (issue #11). Four things matter and none is written down. Views keep whichever security mode they were created with, `DEFINER` or `INVOKER`, and the connector stores that mode without enforcing any policy on it. View definitions have no overall length check and are all held in memory, so a large or numerous set of definitions is a resource risk. Filesystem storage needs Trino to read and write its directory, and anyone else who can write there can change views. Anyone with write access can also stop the catalog from loading: one file or row that fails to parse fails the startup load of every view. The repository also has no vulnerability-reporting policy: private vulnerability reporting and Dependabot alerts are off, and code scanning is not configured. Secret scanning and push protection are already on.

## Preferred approach: a SECURITY.md that documents current behavior

A `SECURITY.md` at the repository root, in GitHub's conventional form, so it appears in the repository's Security tab. It states how to report a vulnerability, then documents the connector's security properties as they are today. Turning on Dependabot alerts and code scanning is a repository-settings task in the burndown, not text in the guide.

| Aspect | Detail |
|---|---|
| Location | Repository root on `v479`, the default branch, which is where GitHub reads it |
| Reporting | How to report privately (GitHub private vulnerability reporting), and which version branches are supported |
| Security modes | Both `DEFINER` and `INVOKER` are stored and returned unchanged; the connector enforces no policy on them |
| Resource limits | Names are capped at 100 characters, but a definition's length is not, and every definition is held in memory |
| Filesystem storage | Trino needs read and write access to `viewzoo.dir`; anyone with write access can add, change or remove views, and a malformed file stops the catalog from loading |
| JDBC storage | The JDBC user needs to create, read and write the `viewzoo` table; anyone with write access to that table can change views, and a malformed row stops the catalog from loading; keep the password out of plain-text catalog files using Trino's secret substitution |

- **Documents, doesn't change** — the guide describes the code as it is, so it can ship now and change as features land.
- **Write access is the real boundary** — whoever can write the storage can change what every query through a `DEFINER` view runs as, which is the most important thing for an operator to know.

## Alternatives considered

- **Add a definition length check in the same item** — closes the gap instead of documenting it, but it is a code change with its own limit to choose, and it would hold back the guide. It can become its own work item.
- **Put the security material in the README** — rejected because GitHub surfaces `SECURITY.md` specifically, and the README is already being reworked by another item.

## What this doesn't solve

- The missing length check remains; only the guide mentions it.
- Policy on security modes stays unenforced until #13 is decided.
- The guide has to be carried forward to each new version branch, and updated when the default branch changes.
