# Modernize: Implementation Plan

## Objective

Bring ViewMapper's Claude integration, MCP server and image up to current practice, keeping the architecture: explicit effort, thinking blocks returned across tool calls, refusal handling, timeouts for thinking models, an audited system prompt, MCP Python SDK 2.x, and a pinned current base image. Make failures unmistakable to the client (#8), and diagrams render rather than show as source (#7). Targets the `v483` branch, released as `483b` or later. The default model stays Sonnet 5.5.

## Context

See `VMR_MODERNIZE_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VMR_SCOPE.md` — problem space this fits into
- `VMR_FINDINGS.md` — relevant prior decisions
- `VMR_APPROACH.md` — design constraints

## What changes

- Agent:
  - `pom.xml` — replace LangChain4j with `anthropic-java`.
  - `ViewMapperAgent.java` — the SDK's tool runner, effort, thinking blocks returned across tool calls, refusal handling with server-side fallback, and a test seam that keeps the reasoning layer testable without API calls.
  - The six tool executors — re-declared as the SDK's annotated tool classes, keeping their contracts.
  - `AnthropicConfig.java` — effort and timeout settings, with environment overrides alongside `ANTHROPIC_MODEL`.
  - The system prompt — audited against current prompting guidance, then rewritten where it over-prescribes.
- MCP server:
  - `pyproject.toml` — `mcp` 2.x.
  - `mcp_server.py` — run on 2.x; the low-level `Server` and `stdio_server` it uses still exist there. Set the subprocess timeout to match the agent. Return failures, timeouts included, as tool errors with `isError` (#8).
  - The tool description — say that an error result means the question wasn't answered and must not be answered from earlier results (#8), and steer the client to render Mermaid output (#7).
- Agent: connection failures name the likely cause, such as a malformed URL or an unreachable host, instead of passing through the driver's message (#8).
- `Dockerfile` — both stages on one pinned, current Ubuntu base.
- Docs — environment variables, the default model, and timeouts.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `MockChatModel` and the agent tests | Depend on LangChain4j's `ChatModel` | Replaced by a new seam that keeps tests free of API calls |
| The six tool executors | Registered by LangChain4j's `@Tool` | Re-declared for the SDK's tool runner; each keeps a test that goes through the runner's JSON deserialization |
| MCP server's conversation history | Replayed into each subprocess call | Must keep working under the 2.x API |

## Testing approach

Unit tests with a mock model stay green, plus new cases for refusals and timeouts. The MCP server's `pytest` suite is ported to 2.x. Live checks with a real API key confirm that Sonnet 5.5 calls the tools on all four bundled datasets at the chosen effort. They also record time and cost per question, so effort is chosen by measurement. MCP tests cover a failing subprocess returning a tool error. Manual Claude Desktop checks go in `VMR_MODERNIZE_TESTING.md`, including a malformed connection URL (#8) and a plain request for a diagram that should render without asking for a file (#7).

## Implementation sequence

1. Agent: move to `anthropic-java`, effort, thinking blocks, refusals, timeouts.
2. System prompt audit and rewrite, checked live on all four datasets.
3. MCP server on 2.x.
4. Docker base, docs, and release.

## Scope boundary — what this does NOT include

- New tools, new analysis features, or changes to the two-module architecture.
- Support for non-Claude models.
- The Trino upgrade and default-model swap, which are `VMR_TRINO_483`.

## Open issues

1. Which effort level for Sonnet 5.5. Its default is `high`; start the measurement at `medium` for multistep tool use.
2. Timeout values for the agent and the MCP subprocess, and whether a long question should report progress rather than just wait.
3. Whether MCP 2.x offers an output form that Claude Desktop renders as a diagram more reliably than Mermaid text (#7).
