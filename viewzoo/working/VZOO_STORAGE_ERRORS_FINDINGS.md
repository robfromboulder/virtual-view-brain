# Storage Errors: Decision Record

## Problem

Both storage clients' `getViews` run when `ViewZooMetadata` is constructed and throw on the first entry that fails to read or parse, so one bad row or file makes every view in the catalog unusable (#25, and the first item in #24's comments). Anyone who can write one bad entry to storage, or one write that fails partway, can take the whole catalog offline: a denial of service, which Rob ranks a severe security issue. Separately, the clients wrap exceptions in `TrinoException` without their cause, so the stack trace, the JDBC SQLState and, for the filesystem, even the message are lost (#24).

## Preferred approach: skip and log, always

An entry that can't be read or parsed is logged and skipped; the rest of the catalog loads. This is a fixed policy for both clients, not a choice to make per case (Rob). Failures that aren't about one entry — the directory missing or unwritable, the database unreachable, the query failing — still fail the catalog, because no partial result would be meaningful.

| Aspect | Detail |
|---|---|
| Scope of a skip | One file or one row |
| What still fails load | Directory checks, connection and query failures |
| Visibility | A warning naming the entry and the exception |
| Exception wrapping | Every `TrinoException` from storage carries `e` as its cause |

- **Availability** — no single entry can brick the catalog, matching the skip-with-warning rule PR #27 already applies to unloadable file names.
- **Consistency** — both clients follow one policy, so behavior doesn't depend on storage type.
- **Diagnosability** — preserved causes give operators the stack trace and SQLState, which `VZOO_SAFE_CREATE` also needs to map a JDBC unique violation.

## Alternatives considered

- **Fail loudly** — keeps a corrupt entry from going unnoticed, but lets one entry deny service to every view. Rejected as a security issue (Rob).
- **Configurable policy** — a flag to choose fail or skip. Rejected: the failing mode is never the safe one, and a flag is one more thing to set wrong.
- **Quarantine or repair the bad entry** — renaming or deleting it on load. Rejected: load would then modify storage, and a hand-edited file may be one fix away from valid.

## What this doesn't solve

- A skipped view silently disappears from SQL; only the log says why.
- A definition that parses but whose SQL no longer works still fails only when queried.
- Truncated files can still be written until `VZOO_SAFE_CREATE` makes filesystem writes atomic; this item only stops them from breaking load.

## Reversals

`VZOO_FINDINGS.md`, the finding that storage-first ordering requires all-or-nothing writes, says a failed filesystem write "leaves a corrupt file that stops the catalog from loading on restart (#28)". After this item the corrupt file is skipped, losing only that view; reconcile the claim at closeout.
