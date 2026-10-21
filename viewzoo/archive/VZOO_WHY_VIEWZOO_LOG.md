# Why ViewZoo: Session Log

Running log of implementation sessions. Each session appends after a `---` separator.

The first entry, and every one after it, follows the entry format and content rules in `VV_SESSION_CLOSEOUT.md` — that spec is the authority, not the prior entry, since a fresh LOG file has none to copy.

---

# README positioning drafted, draft PR opened (2026-10-20)

**Session ID**: `19cc9c04-a31d-4262-bb18-99f76d6043eb`

Rob Dickinson (robfromboulder), with Claude as co-author, drafted the README's "Why ViewZoo?" section, checked its claims and the PostgreSQL connector example, and opened draft PR #35 against `v483`.

## Lineage

- Rob asked for README changes from the work item, considering both text and the hero SVG. Claude created `why-viewzoo` and drafted the plan's four changes: a "Why ViewZoo?" section near the top, workflow framing for the two storage intros, the PostgreSQL connector pairing (placed inside the JDBC section rather than as its own section), and a startup-load caution in Limitations.
- Claude recommended leaving the hero unchanged. Its tagline already matches the positioning, its enclosures are labeled neutrally with no development or production framing, and the visual design rule that only the opening sheet is drawn argues against drawing the comparison. Claude flagged the title block's "500+ VIEWS" scale as the hero's least defensible claim, since nobody has measured view counts; it's outside this item.
- Against the Trino 483 docs, the PostgreSQL connector has no view management and the Iceberg JDBC catalog requires `default-warehouse-dir`; the docs say nothing on that catalog's view support.
- Rob had Claude run the PostgreSQL connector check against the docker-compose stack with a temporary `pg.properties`. The README query listed the stored views, and a row inserted straight into `viewzoo` appeared only after a Trino restart, confirming the new caution.
- Rob moved "Why ViewZoo?" to the end of the README. Rob then noticed the git workflow had shrunk to one sentence; Claude moved both storage modes' reasons into "Why ViewZoo?" and reduced the intros to how each mode stores views.
- Rob proposed collapsing the section into a two-column table of where views are stored and their tradeoffs, then edited it directly. Claude reviewed those edits: two spelling slips, the dropped fact that the PostgreSQL connector can't create Trino views, and unsupported comparatives ("better than Hive", "most expensive"). Rob kept the memory-connector performance line they had written and "highest complexity" for REST, and had Claude apply the rest.
- Rob asked for a fact or two more per row, each with its own storyline, crediting what each option does well. Claude added cost for memory, fit for native Postgres views, scale and a failure mode for Hive, the no-service upside for Iceberg JDBC, governance for REST, recovery from git for filesystem storage, and outage behavior for JDBC storage. Claude corrected its own filesystem claim to cover only committed views, since nothing commits a view created through SQL.
- Rob asked Claude to check the new claims. All held: Trino's memory, Hive and metastore docs (metastore caching is off by default, so a metastore outage fails lookups), the Hive admin manual, Spark's Hive docs, the Iceberg REST spec, Iceberg's `JdbcUtil` (rows store a `metadata_location`, and views are stored too), and the Polaris and Lakekeeper docs. Claude committed the README and opened #35.

## Decisions

- Rob: "Why ViewZoo?" is the last section, and the storage-mode reasons live in its table rather than in the storage intros. Both are recorded as deviations in the burndown.
- Rob: each table row credits the option's strengths as well as its drawbacks, so neighbors read as different tradeoffs rather than worse choices.

## Lessons

- A "tradeoffs" column that lists only ViewZoo's benefits reads as a pitch; ViewZoo's rows carry the startup-load cost and the container volume requirement too.

## Open threads

- The GitHub rendering check in the testing plan is not yet run.
- Whether `pg.properties` ships in `src/test/docker` is still Rob's call.
