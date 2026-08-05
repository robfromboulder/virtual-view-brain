# Virtual View Manifesto: Scoping Statement

> V5, 2026-08-02.

This document defines the problem the manifesto addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states one part of the problem the ecosystem's scoping statement defines: the part where the practice is unwritten.

---

## 1. Problem Statement

Nobody has written down how to use views as architecture. The mechanics are documented by every engine, and the conventions that make a hierarchy survive contact with a real system are documented by none: how to organize views so they abstract rather than mirror storage, how many versions a view should expect to have, who owns a layer, what breaks a hierarchy and how quietly. A practitioner willing to try the pattern has to derive all of it, and the derivation costs more than most teams will spend on a hunch.

The reader arrives skeptical, and reasonably so. They already have ORMs, microservices and data access layers, all of which decouple applications from storage, and all of which are better documented than this. Any account of the pattern that does not deal with those alternatives honestly reads as advocacy and gets dismissed. So the problem is not only to state the pattern but to make it survive a hostile first reading, which means being candid about where the pattern does not pay and about the sharp edges it cannot file down.

---

## 2. State of the Problem

### What exists to read

Documentation of SQL views is documentation of the feature: syntax, permissions, and the classical uses — hiding a join, computing a column, restricting a set of rows. Material on decoupling applications from storage is abundant and concerns ORMs, service boundaries and data access layers. The intersection, using views themselves as the abstraction, has no canonical text. A practitioner searching for it finds vendor feature pages and blog posts about the classical uses.

The consequence is that the pattern has no shared vocabulary. Two teams doing the same thing describe it differently, and neither can point at a document to settle what the practice is.

### Who has this problem

Trino users first: full-stack engineers, application architects and big-data practitioners, working in systems where SQL is the native query language rather than something an ORM generates. They know what a view is and have never considered one architecturally, which means the account has to bridge from the classical use they already have rather than starting from the pattern.

They want practical guidance rather than theory, and they read technical detail and concrete examples as evidence that the author has actually done this. They also arrive holding working alternatives, which sets the bar: the pattern has to be shown doing something those alternatives do not.

### What the audience is becoming

A reader may consult the text directly or put an agent between themselves and it, and the second path asks different things of the writing. A document that only pays off when read cover to cover cannot answer a question posed against it; one written to be queried — consistent terminology, self-contained examples, explicit conditions on every recommendation — serves both readings. Which path a given reader takes is not something the text controls, so the demand holds whether or not anything is built for it.

### What the practice lacks besides prose

The failure modes are silent ones. A replaced view with a changed column type breaks its dependents at query time rather than at replacement time, and no engine warns anyone. Ownership of a layer is a convention with no enforcement behind it. Prose is the only place these can be addressed, because there is no mechanism to appeal to.

---

## 3. Goals

A reader finishes and:

- Understands virtual views as an architectural pattern rather than a database feature or a Trino trick.
- Can carry a feature through the progression the pattern enables, from static data to a live source, without a redesign at each step.
- Knows the cases where the pattern is the wrong choice, and can say why.
- Knows which failure the discipline around each principle prevents, rather than holding a list of rules to comply with.

A skeptic finishes and disagrees on substance rather than dismissing the piece as advocacy.

An agent asked a question about the pattern can answer it from the text, without the asker having read it first.

---

## 4. What Is Not In Scope

- **Restating Trino.** Federation, connectors and query behavior are Trino's documentation to write. The subject is what the pattern adds on top.
- **Installation and configuration.** Tooling carries its own setup instructions, and duplicating them here would rot.
- **Academic framing.** No formalism, no literature survey, no theory for its own sake.
- **Empirical claims without evidence.** Assertions about adoption, performance or prevalence that cannot be backed are out, because they are the easiest thing for a skeptic to pull on.
- **Automating the practice.** Turning the pattern into something an agent executes rather than explains is a different problem with a different audience.

---

## 5. Open Questions

- Whether serving agent readers well requires anything beyond writing precisely for human ones. The two demands look aligned and have not been tested against each other.
- Whether a body of applied material — recipes rather than argument — belongs in this project at all. It would be a second product with a second audience, and the answer changes what completion means here.
- Whether the reader who needs convincing and the reader who needs instructions are the same person. If they are not, serving both from one body of material may be working against itself.
