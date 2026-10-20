# Security Mode: Decision Record

## Problem

A `DEFINER` view runs as the `owner` named in its stored definition. When a view is created through Trino, that owner is the authenticated session user. When it arrives any other way — a file synced from git, a row written straight into the PostgreSQL table — the owner is an unauthenticated string, so anyone who can get a file merged or a row written can create a view that runs as an administrator. The #13 requester migrated from an in-house module and wants to restrict views to `INVOKER` as a security control in addition to PR review, enforced both on create and when the view is used.

## Preferred approach: an optional allowed-mode policy

A catalog property restricts which security modes the connector accepts, defaulting to both. A disallowed view is refused on create; one found in storage is refused or hidden (open in PLAN). A disallowed view is never silently converted.

| Aspect | Detail |
|---|---|
| Default | Both modes, as today |
| Create | Refused before storage is written |
| Stored view | Fail on query or skip on load — open |
| Scope of check | The security mode only |

- **Closes owner spoofing** — with `INVOKER` only, a stored owner grants nothing, whoever wrote the file.
- **Narrow** — the store still judges no view's SQL; it only declines to trust an identity it can't verify.
- **Opt-in** — catalogs that don't set it behave exactly as before.

## Alternatives considered

- **Silently rewrite `DEFINER` to `INVOKER`** — the view's description and its execution would disagree; rejected, as the #13 requester also concluded.
- **Leave it to Trino access control** — the right layer if Trino can forbid `DEFINER` views globally, which is still to be checked. The #13 discussion noted `checkCanViewQueryOwnedBy` would need Trino core to expose the security mode.
- **Enforce only by PR review** — works where every write goes through review, but not for JDBC rows or a directory writable by others.

## What this doesn't solve

- `INVOKER` views still run whatever SQL the stored definition holds, with the querying user's privileges.
- Who can write storage remains the real boundary; this removes one thing a writer can gain, not their access.

## Reversals

- `VZOO_APPROACH.md`, Key Design Decisions — "The store holds what it is given and judges none of it", with the security mode "carried rather than checked." Becomes optionally checked. Closeout should restate the principle as judging no view's content while declining to trust an unverifiable owner, and answer the matching question in `VZOO_SCOPE.md`'s Open Questions on whether the store enforces policy.
