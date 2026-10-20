# Storage Errors: Decision Record

## Problem

Both storage clients' `getViews` run when `ViewZooMetadata` is constructed and throw on the first entry that fails to read or parse, so one bad row or file makes every view in the catalog unusable (#25, and the first item in #24's comments). Measured on Trino 483: a catalog whose connector fails to construct stops the whole server at startup (exit 100), so one bad entry takes down every catalog, not only ViewZoo's. A definition of `null` loads, but `information_schema.views` then fails for the catalog and `SHOW TABLES` lists a view that can't be queried. Anyone who can write one bad entry to storage, or one write that fails partway, can take the whole catalog offline: a denial of service, which Rob ranks a severe security issue. Separately, the clients wrap exceptions in `TrinoException` without their cause, so the stack trace, the JDBC SQLState and, for the filesystem, even the message are lost (#24).

## Preferred approach: skip and log, always

An entry that can't be read, parsed or keyed is logged and skipped; the rest of the catalog loads. This is a fixed policy for both clients, not a choice to make per case (Rob). Failures that aren't about one entry — the directory missing or unwritable, the database unreachable, the query failing — still fail the catalog, because no partial result would be meaningful.

| Aspect | Detail |
|---|---|
| Scope of a skip | One file or one row |
| What counts as a bad entry | A read or parse that throws, a parse that returns null, and for JDBC a NULL definition or a schema or view name that is empty or not lowercase |
| What still fails load | Directory checks, connection and query failures |
| Visibility | A warning naming the entry and the exception message, without a stack trace |
| Exception wrapping | Every `TrinoException` from storage carries `e` as its cause |

- **Not only exceptions** — the JSON literal `null` parses without error to a null definition, and a null in the cache fails every listing of the catalog, so a null result is a bad entry too. A NULL `definition` column and an empty name throw `IllegalArgumentException`, not a parse exception, so JDBC catches per row rather than by exception type.
- **JDBC names follow the filesystem's loadable-name rule** — `SchemaTableName` lowercases, but the JDBC primary key is case-sensitive, so an uppercase row would load under a name that drop and rename miss, and would silently replace a lowercase row of the same name. Skipping non-lowercase rows also means no two entries in either storage type can resolve to one view, so duplicates need no separate rule.
- **Bounded log lines** — Jackson 2.22 redacts the source from its messages and truncates echoed tokens (a 100 KB invalid token gives a 468-character message), so logging the message can't leak or flood with a definition.

- **Availability** — no single entry can brick the catalog, matching the skip-with-warning rule PR #27 already applies to unloadable file names.
- **Consistency** — both clients follow one policy, so behavior doesn't depend on storage type.
- **Diagnosability** — preserved causes give operators the stack trace and SQLState, which `VZOO_SAFE_CREATE` also needs to map a JDBC unique violation.

## Alternatives considered

- **Fail loudly** — keeps a corrupt entry from going unnoticed, but lets one entry deny service to every view. Rejected as a security issue (Rob).
- **Configurable policy** — a flag to choose fail or skip. Rejected: the failing mode is never the safe one, and a flag is one more thing to set wrong.
- **Quarantine or repair the bad entry** — renaming or deleting it on load. Rejected: load would then modify storage, and a hand-edited file may be one fix away from valid.

## What this doesn't solve

- A skipped view silently disappears from SQL; only the log says why.
- A skipped entry stays in storage, so `DROP VIEW` of its name reports it doesn't exist and a rename onto its name reports it already exists; removing it means editing storage directly.
- A JDBC row with a mixed-case name, which loaded under its lowercased name before, is skipped after upgrading. Only a row written outside Trino can have one, since Trino lowercases every name ViewZoo stores, and such a row was already broken: drop, rename and replace missed it.
- A definition that parses but whose SQL no longer works still fails only when queried.
- Truncated files can still be written until `VZOO_SAFE_CREATE` makes filesystem writes atomic; this item only stops them from breaking load.
- Until `VZOO_SAFE_CREATE` makes storage refuse a create without `OR REPLACE`, a plain `CREATE VIEW` of a skipped entry's name silently overwrites that entry in both storage types, losing a hand-edited file that may be one fix away from valid.

## Reversals

`VZOO_FINDINGS.md`, the finding that storage-first ordering requires all-or-nothing writes, says a failed filesystem write "leaves a corrupt file that stops the catalog from loading on restart (#28)". After this item the corrupt file is skipped, losing only that view; reconcile the claim at closeout.
