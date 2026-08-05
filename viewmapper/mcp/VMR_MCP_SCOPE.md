# ViewMapper MCP Server: Scoping Statement

> V5, 2026-08-02.

This document defines the problem that the MCP server addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states the conversational half of the problem ViewMapper's scoping statement defines.

---

## 1. Problem Statement

Analysis that runs as a one-shot command cannot be explored. Exploration is a sequence of dependent questions — "what's here", "focus on that one", "go one level further" — and each of those is unanswerable without what came before. A program that answers the question it was given and forgets leaves the thread to be held by something else.

Three further problems come from the destination rather than the source. The client is a chat application that speaks a protocol, so there is a surface to implement and conform to. The client also decides how output is displayed, and a diagram that arrives in a form the client treats as source code is a diagram the user has to render themselves — technically correct and practically useless. And the user is in a chat window with no terminal and no logs, so a failure that surfaces as a stack trace or a silent hang leaves them nothing to act on.

The last constraint is on size. Whatever bridges these two worlds sits between a protocol that changes and analysis that changes, and every capability it grows is a capability that has to be kept in step with both.

---

## 2. State of the Problem

### What the protocol provides

MCP is the established way a chat client reaches an external tool, with SDKs that make conformance a small amount of code rather than a project. It defines how tools are advertised, called and answered.

It does not carry a session identity that a server can key on. Every conversation a client opens arrives looking the same, so a server holding per-conversation state has nothing to distinguish one from another.

### What the client controls

Display. The same text can render as a diagram or print as source depending on how the client classifies it, and that classification responds to how the user phrases the request rather than to anything the server declares. A user who asks for a "diagram" and a user who asks for a "diagram file" get materially different experiences from identical output.

The client is also the entire interface. There is no terminal beside it, no log file the user will open, and no exit code they will see. A failure is whatever text appears in the chat.

### What the user is expected to have

Chat client users are not developers of this tool and often not developers at all. Requiring a language runtime, a build toolchain or a dependency install on their machine is a barrier out of proportion to the task of asking about a schema.

### What one-shot execution costs

Starting a fresh process per question pays a fixed cost every time, and that startup is measured in seconds rather than milliseconds. Against analysis that itself takes tens of seconds on a large schema this is a fraction of the wait, and it is a fraction paid on every single question including trivial ones.

### What a person will wait

Somewhere under a minute before assuming the thing is broken. That ceiling is a property of the user, not of the workload, and any bound chosen has to sit under it while still covering the slow legitimate cases.

---

## 3. Goals

- A follow-up question that refers to a previous answer is understood as a follow-up.
- A diagram arrives in a form the client shows, without the user knowing which phrasing makes that happen.
- A failure produces something the user can act on from inside a chat window.
- Someone can use this without installing a language runtime, a build toolchain, or project dependencies.
- Keeping up with changes on either side — the protocol or the analysis — stays cheap.

---

## 4. What Is Not In Scope

- **Analysis.** No SQL parsing, no graph work, no reasoning about schemas.
- **Persistence.** Conversation state is not expected to survive the process.
- **Clients other than Claude Desktop.** The protocol is general; the target is not.
- **Concurrency.** One conversation at a time.

---

## 5. Open Questions

- Whether rendering can be made independent of the user's phrasing from the server side at all, or whether it is client behavior that no server-side change can reach.
- Whether conversations sharing one history is a real problem in practice. It is a known consequence of the protocol carrying no session identity, and no user has reported hitting it.
- What the right time bound is, given that the slowest legitimate case has never been measured on a schema large enough to be representative.
- Whether the per-question startup cost is worth removing, which would mean keeping a process alive between questions and giving up the property that each question is answered from a clean slate.
