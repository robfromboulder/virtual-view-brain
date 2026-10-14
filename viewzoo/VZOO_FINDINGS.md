# ViewZoo: Implementation Findings

> V3, 2026-10-13.

Findings made during implementation that are not evident from reading the code. Each entry names the options considered and the reason the chosen approach won. Assume the current codebase is available as ground truth — this document does not restate what the code already shows.

---

## 1. READ_COMMITTED is the only declared isolation level

The connector reports READ_COMMITTED because that is the least restrictive level Trino accepts, and nothing about the store's behavior would differ under a stricter one. View operations are synchronized and served from an in-memory map, so there is no concurrent-read anomaly to prevent and no write ordering beyond the lock. Declaring a stricter level would promise semantics the store does not implement; READ_COMMITTED matches what actually happens.

---

## 2. A Trino upgrade aligns runtime-supplied dependencies to Trino, not to their newest releases

Slice, `jackson-annotations` and OpenTelemetry are supplied by Trino at runtime, so the pom pins them to the versions the target Trino release ships (its Airbase), and Airlift to the version Trino itself uses. Only the PostgreSQL driver is bundled with the plugin, so it alone moves to its current release. Maven Central's search API lags new releases; confirm a dependency's current version from the repository's `maven-metadata.xml`. Established by the Trino 483 upgrade (PR #15, `2b3240a`).

Trino's plugin loader performs no SPI version check, so a build for one release can load into another; passing integration tests against a newer Trino image is how to tell whether an upgrade needs source changes or only version bumps. The 479 build passed all integration tests against Trino 483 unmodified.

## 3. `hero.svg` carries its text as outlined paths

The README hero image draws its text as glyph outlines, so a text search for a version number or date misses it; only `hero.src.svg` holds the text as `<text>`. A version sweep must search `hero.src.svg`. Re-rendering `hero.svg` from the source with Inkscape alters the artwork (rounded enclosure corners, lost SQL indentation), so until the original render tool is known, change its text by outlining only the affected strings and swapping those paths in at their existing positions. Established by the 483 badge fix (PR #15, `f376256`).
