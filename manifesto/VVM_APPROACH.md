# Virtual View Manifesto: Technical Approach

> V4, 2026-08-02.

This document describes the proposed approach for addressing the problems defined in `VVM_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

Write for the skeptic, not the convert. The reader who already has an ORM is the one worth convincing, so alternatives are acknowledged before the pattern is argued, and the argument shows where virtual views complement what a reader already runs rather than where they replace it. Limitations are stated plainly, including the ones with no fix, where the honest answer is a discipline rather than a guarantee. Anything a reader could dispute and win is cut, which rules out claims about how many teams do what.

The voice is strongly opinionated but not fundamentalist, pragmatic rather than dogmatic, plain in language and sentence construction, and third-person throughout: no "I", no "we". "Manifesto" is tongue-in-cheek, chosen to get attention onto a topic readers expect to be boring, and the humor stays sparing enough that the document reads as clean and precise rather than clever. Em dashes are barred outright, on the grounds that they break web rendering and read as machine-written.

When work has to be traded off, accuracy and terminology consistency come first, conciseness and logical flow second, and creativity only when it is asked for.

The editorial check that matches this strategy is an adversarial one: the draft is reviewed in the voice of a reader looking for grounds to dismiss it, hunting sequencing problems, unaddressed counterarguments, unfounded claims, missing context, and defensive posturing.

---

## 2. Architecture

The published artifact is a single README, generated from ten ordered section files rather than edited directly. Keeping the sections separate is what makes the document reorderable and reviewable in pieces, and the generated README is what GitHub renders, so it stays committed alongside its sources.

The order is the argument. The introduction establishes classical views and their cost, the principles state the pattern, the use cases show where it pays, the implementation guide walks one worked example end to end, and the pitfalls and anti-patterns close by naming where it does not pay. Related tools come after the reader is persuaded rather than before, and the glossary catches the terms the argument introduced.

---

## 3. Key Design Decisions

**Trino is the reference implementation, and the concepts are stated as portable.** Federation is what makes Trino a good stage for the pattern: multi-source examples are natural rather than contrived. Every example is written and validated against Trino, while the prose stays careful that the ideas apply to any database with views.

**A use case must show something you could not easily do without virtual views.** This is the sharpest editorial rule, and it excludes material that would otherwise be attractive: cross-database federation demonstrates beautifully and is a Trino capability rather than evidence for the pattern. What qualifies is swappable implementations, independently evolving layers, static-to-live progressions, and runtime reconfiguration.

**Terminology is fixed by table, not by ear.** Virtual views over logical views, because the point is detachment from the physical. Base view over parent view, and layer over level, because a layer implies responsibility rather than position. Swappable over replaceable, because the point is that it was designed for. Federation over data virtualization, and "virtualizing at the query engine layer" over "database abstraction layer", because both alternatives are vaguer about where in the stack the work happens.

**Every SQL example uses the same three-level naming convention**, with physical objects as `connector.schema.table` and virtual ones as `catalog.schema.view`, and a schema promoted to a catalog when it crosses over. Repetition is the mechanism: the transformation is taught by every example showing it rather than by any passage explaining it. The same reasoning puts `SECURITY INVOKER` on every `CREATE VIEW` example except where the counter-example is the point.

**The document is the agent interface, and nothing more is built.** Handing the manifesto to Claude and asking questions of it works today, unaided, because the qualities that serve a skeptical human reader — fixed terminology, self-contained examples, explicit conditions on every recommendation — are the same ones that make a text answerable. No agentic workflow is defined over this material, no cookbook exists, and no interface is planned. The position is that the writing standard already does this job, held until something shows it does not.

**Major points get a simple example and a realistic one.** The simple example makes the mechanism legible in a few lines; the realistic one shows the shape that mechanism takes under production complexity. Neither alone convinces the target reader.

---

## 4. What We Build

A single document, published as a GitHub README and generated from its section files, carrying the argument for the pattern, its principles, the cases for and against it, a worked implementation example, and a glossary. It links out to the tools that handle what prose cannot, and it ships no code of its own.
