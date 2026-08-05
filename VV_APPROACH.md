# Virtual View: Technical Approach

> V3, 2026-08-02.

This document describes the proposed approach for addressing the problems defined in `VV_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

One obstacle, one project. The manifesto removes the unwritten practice, ViewMapper removes the invisibility of a built hierarchy, and ViewZoo removes the storage tax. Each is adopted on its own and is useful with none of the others installed, because a team meets the three obstacles in an order nobody controls and the goal is that clearing one is enough to keep going. A single combined product would invert that: it would demand all three commitments at the moment a team wants one, which is the kind of cost the pattern exists to avoid.

Trino is the only supported platform, though the pattern itself ports to any engine with SQL views. Committing to one engine is what makes the claims testable — every example runs, and every behavior asserted about view replacement can be checked. Compatibility with Starburst Enterprise and Galaxy is acknowledged where it comes up, and never as a support claim; all three repositories carry that disclaimer.

None of this is a product. Everything is free and unaccompanied by a service, and the licensing splits along the same line: CC0 for the manifesto, which puts the pattern in the public domain to be quoted and adapted without attribution mechanics, and Apache 2 for the two code projects. That suits an audience of SQL-native practitioners evaluating an architectural pattern rather than buying a platform.

---

## 2. Architecture

The manifesto is the entry point and the only piece that names the others. Its principles reach a tool at exactly the two points where a tool is the answer: the principle requiring a canonical location for view definitions links to ViewZoo, and the principle to map complexity rather than memorize it links to ViewMapper. Everything before those two points costs a reader nothing and installs nothing.

The dependency direction is one-way and shallow. The manifesto points at both tools; neither tool points back, and neither requires the other. ViewMapper reads view definitions through Trino over JDBC, so it maps any hierarchy in any connector, whether or not ViewZoo stores it. ViewZoo persists view definitions for Trino and knows nothing about the pattern or the mapper. Their only meeting point is Trino itself, which is what lets a team adopt either one alone.

ViewMapper's examples use `viewzoo.*` schemas. That is convenient sample data, not a dependency, and it is worth saying because it reads like one.

---

## 3. Key Design Decisions

**Three repositories rather than one.** The pieces have different audiences, different stacks, and unrelated release cadences — a book, a Java agent with a Python MCP wrapper, and a Trino plugin. Separate repositories let each move at its own speed and let a reader take the book without cloning a connector.

**No coupling between the tools.** ViewMapper could read stored definitions directly from whatever holds them, and instead goes through Trino's metadata. Universality is worth more than the shortcut: a mapper that understood ViewZoo's storage would be a mapper that only works on hierarchies ViewZoo stores, which contradicts adopting either tool alone.

**Different release strategies for the two code projects, deliberately.** ViewZoo compiles against the Trino SPI, which breaks between Trino versions, so it takes the Trino version as its own version number and keeps a branch per supported version — v470 through v479 today. ViewMapper connects over JDBC and carries no such constraint, so it moves `main` forward and tags releases with the Trino version plus a letter, as in `479a`. The projects are on the same Trino version today; nothing in the design requires them to stay in step, and work targeting either one names the Trino version it assumes.

---

## 4. What We Build

- **Manifesto** — prose that states the pattern, its principles, the use cases where it pays, and the cases where it does not.
- **ViewMapper** — an agent that extracts view-to-view dependencies from Trino and produces navigable diagrams of the resulting graph.
- **ViewZoo** — a Trino connector that stores view definitions on the filesystem or in Postgres, with no metastore and no object storage.
