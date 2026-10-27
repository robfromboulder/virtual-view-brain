# ViewMapper MCP Server: Scoping Statement

> V6, 2026-10-27.

This document defines the problem that the MCP server addresses, separately from design decisions and implementation details, as an objective and unbiased resource. It states the conversational half of the problem ViewMapper's scoping statement defines.

---

## 1. Problem Statement

Analysis that runs as a one-shot command cannot be explored. Exploration is a sequence of dependent questions — "what's here", "focus on that one", "go one level further" — and each of those is unanswerable without what came before. A program that answers the question it was given and forgets leaves the thread to be held by something else.

ViewMapper's design gives this module the conversational half, a chat client to serve, and analysis reached through a subprocess call, and those are given here.

Three further problems come from the destination rather than the source. The client is a chat application that speaks a protocol, so there is a surface to implement and conform to. The client also decides how output is displayed, and a diagram that arrives in a form the client treats as source code is a diagram the user has to render themselves — technically correct and practically useless. And the user is in a chat window with no terminal and no logs, so a failure that surfaces as a stack trace or a silent hang leaves them nothing to act on.

The last constraint is on size. Whatever bridges these two worlds sits between a protocol that changes and analysis that changes, and every capability it grows is a capability that has to be kept in step with both.

---

## 2. State of the Problem

### What the protocol provides

MCP is the established way a chat client reaches an external tool, with SDKs that make conformance a small amount of code rather than a project. It defines how tools are advertised, called and answered.

As of October 2026, it identifies no conversation. A session, where the transport has one, belongs to the client's connection rather than to a chat, so every conversation a client opens arrives looking the same, and a server holding per-conversation state has nothing to distinguish one from another.

### What the client controls

Display. The same text can render as a diagram or print as source depending on how the client classifies it, and that classification responds to how the user phrases the request rather than to anything the server declares. A user who asks for a "diagram" and a user who asks for a "diagram file" get materially different experiences from identical output.

The client is also the entire interface. There is no terminal beside it, no log file the user will open, and no exit code they will see. A failure is whatever text appears in the chat.

### What the user is expected to have

Chat client users are not developers of this tool and often not developers at all. Requiring a language runtime, a build toolchain or a dependency install on their machine is a barrier out of proportion to the task of asking about a schema.

### What a person will wait

Somewhere under a minute before assuming the thing is broken. That ceiling is a property of the user, not of the workload.

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

---

## 5. Open Questions

- Whether rendering can be made independent of the user's phrasing from the server side at all, or whether it is client behavior that no server-side change can reach.
