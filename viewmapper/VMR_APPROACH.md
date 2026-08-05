# ViewMapper: Technical Approach

> V4, 2026-08-02.

This document describes the proposed approach for addressing the problems defined in `VMR_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

Build a guide, not a dependency mapper. The distinguishing behavior is that the tool assesses how complex a schema is before it tries to draw it, and when the honest answer is that no single diagram will help, it says so and offers entry points instead. Everything else follows from taking that refusal seriously: a tool that always produces a diagram would be easier to build and would fail exactly where the problem is hardest.

Conversation is the interface because exploration is iterative. A user does not know which view to focus on until they have seen what the schema contains, and each answer changes the next question. That rules out a report generator and argues for something a person talks to.

The project also serves as portfolio work, demonstrating agentic reasoning over a problem space rather than fixed tool invocation, alongside a deliberately polyglot architecture. This is worth recording because it is a second constraint on the design: the agentic path is held even in places where a simpler pipeline would produce a comparable diagram, and that choice is not explicable from the problem alone.

---

## 2. Architecture

Two modules, split by problem rather than by stack. The **agent** owns everything analytical: connecting to Trino, parsing SQL, building and interrogating the dependency graph, and reasoning about what to show. The **MCP server** owns everything conversational: speaking the protocol a chat client expects, carrying context across turns, and delivering output in a form the client will render.

They compose as a subprocess call. The MCP server invokes the agent as a command-line program, passes the user's question as arguments, and returns the text that comes back, diagrams included. There is no port, no daemon, and no shared state — each invocation is complete in itself, and everything that has to persist across turns is held by the conversational side and replayed into the next invocation.

That interface is what keeps the split honest. The agent can be driven from a terminal or another Java program with no chat client involved, and it is tested that way. The conversational side can be exercised against a stubbed subprocess with no Trino and no model in the loop.

---

## 3. Key Design Decisions

**A command-line program rather than a service.** This is a desktop tool, so there is nothing for a persistent service to buy: it opens no ports and presents no network attack surface, it installs as one image rather than a deployment, and either half can be tested alone. The cost is per-invocation startup, paid on every question, and accepted.

**A polyglot split, because each half has an obvious language.** The MCP protocol has a Python SDK that makes the server small; the authoritative Trino SQL parser is Java. Choosing one language for both would mean either reimplementing SQL parsing or hand-rolling the protocol.

**Multi-catalog connections are the recommended default.** A JDBC URL without a catalog lets a user explore anything the server exposes, which suits a read-only tool and matches how people actually arrive — not knowing what is there. A catalog-bound URL stays available for enterprise and regulated environments that need the blast radius fixed at configuration time. The two modes are distinguished by URL shape alone, and that shape determines whether a schema is named `catalog.schema` or bare.

**Discovery is essential rather than optional.** Making multi-catalog the default is what makes it so: a user who connects without naming a catalog has nothing to analyze until something tells them what exists. Discovery also unifies the two connection kinds, so exploring a bundled test dataset follows the same steps as exploring a live server.

**Claude models only, and the output is presented as an aid rather than an authority.** The guidance behavior depends on a model that reasons well about when a diagram would be useless and what to offer instead, and quality on other model families has not been established — other families are believed workable and would need substantial testing to reach parity. The consequence is accepted rather than hidden: a user supplies an Anthropic API key, and results are documented as requiring review by someone qualified before decisions rest on them, because a plausible wrong answer is the failure mode this design cannot rule out.

**Public releases are tagged with the Trino version plus a letter — `479a`, `479b` — and never `latest`.** Users paste a tag into a Claude Desktop config file and keep it for months, so an ambiguous tag would give two users different software under the same name and make caching behavior unpredictable. Local builds use the bare version and never leave the machine.

**Contributions go through Claude Code, design first.** The workflow is to discuss the change, record the design decision, then implement, test and update the documentation in the same session. The intent is that the reasoning behind a change is captured while it is still in someone's head rather than reconstructed later.

---

## 4. What We Build

- **Agent** — the analytical half: Trino connectivity, SQL parsing, dependency graph construction and analysis, and the reasoning that decides what to show.
- **MCP server** — the conversational half: protocol handling, cross-turn context, subprocess execution, and output delivered so a chat client renders it.

Distribution is a single Docker image holding both, configured into Claude Desktop by the user, requiring no development toolchain on their machine.
