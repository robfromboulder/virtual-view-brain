# ViewMapper MCP Server: Technical Approach

> V5, 2026-10-26.

This document describes the proposed approach for addressing the problems defined in `VMR_MCP_SCOPE.md`. It covers architectural approach, key design decisions, and what we build — but not implementation phases or delivery milestones, which are derived from this document separately.

---

## 1. Strategic Approach

Stay thin on purpose. This module's leverage comes from what it declines to do: every behavior it adds is a behavior coupled to analysis it does not own, and would have to be revised whenever that analysis changes. So it handles the protocol, holds the thread of a conversation, runs a subprocess, and hands back what comes out.

Thinness has a price, and it is paid deliberately. Passing conversation history as text rather than as a structured argument means the model sees its own prior turns in a slightly artificial form. Launching a fresh process per question means paying startup on every question. Both were accepted in exchange for a module small enough that changes to analysis rarely reach it.

---

## 2. Architecture

One tool, one subprocess, one buffer.

The **tool surface** is a single entry point taking a natural-language question. There is no vocabulary for a client to learn and no tool schema that has to track analytical capabilities, so a capability added downstream becomes reachable without a change here.

The **context buffer** holds the last three turns and prepends them to the question before each call, which is what turns a sequence of independent invocations into a conversation.

The **subprocess boundary** runs the analysis program, waits with a deadline, and returns its text unchanged, diagrams included. Java is located on the PATH rather than by configuration, so the same code runs in the container and on a developer's machine.

Returning text unchanged is what keeps diagram content intact, and it is also the limit of what this design does about diagrams: whether the client displays one or prints its source is decided by the client from the user's phrasing, and nothing the server returns influences that. The goal of making rendering independent of phrasing is unmet, deliberately, until something shows it is reachable from this side at all.

Error handling wraps all of this, converting a failed launch, a non-zero exit, or an expired deadline into a message that says what happened and what to try.

---

## 3. Key Design Decisions

**Context is passed as prompt text, not as a structured argument.** The alternative was a context parameter on the analysis program plus a memory implementation inside it — cleaner separation, and a change to two modules instead of one. Prompt enhancement took about forty lines, needed no downstream change, kept older versions of the analysis program callable, and left the history visible to the model rather than hidden in a mechanism. The structured version remains the better architecture and stays available if the text approach shows its limits.

**Three turns of history.** Enough for the exploration patterns actually observed — ask what exists, ask about one of them, drill in — while keeping prompts small enough to stay clear of token limits and cheap to send. Longer conversations lose their oldest turns rather than failing.

**A long, configurable deadline.** The deadline is a backstop against a hung run, sized to the longest run the analysis program can legitimately make, and defaults to ten minutes with an environment variable to change it. It began as 60 seconds, set by what a person will wait for, and that was abandoned in ViewMapper PR #10 once a single answer could outlast it. When it expires, the run is killed and the message suggests a simpler question rather than retrying, since a retry would take just as long.

**One shared conversation history.** The protocol exposed no session identity when this was built, so the session key is a constant. The consequence is that two chats exploring different schemas share context. This is a known defect held rather than fixed, because the failure is rare — users explore one schema at a time — and because the fix belongs in the protocol.

**A fresh process per question.** Keeping a process warm would remove three to five seconds per question and would introduce lifecycle to manage, state to leak between questions, and a failure mode where the long-lived process is wedged. For a tool answering a handful of questions per exploration, the startup cost is the cheaper problem.

**What this design does not cover.** Claude Desktop is the only client tested and validated, though the protocol is general. Conversation state does not survive the process, and the server serves one conversation at a time.

---

## 4. What We Build

A Python MCP server exposing one natural-language tool, maintaining a three-turn conversation buffer, executing the analysis program as a subprocess under a deadline, returning its text output verbatim so diagrams survive intact, and converting failures into messages a user can act on from a chat window.
