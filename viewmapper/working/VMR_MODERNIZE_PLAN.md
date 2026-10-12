# Modernize: Implementation Plan

## Objective

Bring ViewMapper's Claude integration, MCP server and image up to current practice, keeping the architecture: explicit effort, thinking blocks returned across tool calls, refusal handling, timeouts for thinking models, an audited system prompt, MCP Python SDK 2.x, and a pinned current base image. Targets the `v483` branch, released as `483b` or later. The default model stays Sonnet 5.5.

## Context

See `VMR_MODERNIZE_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VMR_SCOPE.md` — problem space this fits into
- `VMR_FINDINGS.md` — relevant prior decisions
- `VMR_APPROACH.md` — design constraints

## What changes

- Agent:
  - `pom.xml` — LangChain4j to 1.22, or replace it with `anthropic-java`.
  - `ViewMapperAgent.java` — effort, thinking blocks returned across tool calls, refusal handling, and a test seam that keeps the reasoning layer testable without API calls.
  - `AnthropicConfig.java` — effort and timeout settings, with environment overrides alongside `ANTHROPIC_MODEL`.
  - The system prompt — audited against current prompting guidance, then rewritten where it over-prescribes.
- MCP server:
  - `pyproject.toml` — `mcp` 2.x.
  - `mcp_server.py` — run on 2.x; the low-level `Server` and `stdio_server` it uses still exist there. Set the subprocess timeout to match the agent.
- `Dockerfile` — both stages on one pinned, current Ubuntu base.
- Docs — environment variables, the default model, and timeouts.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `MockChatModel` and the agent tests | Depend on LangChain4j's `ChatModel` | Moving to the official SDK needs a new seam to keep tests free of API calls |
| The six tool executors | Registered by annotation | Have to keep their contracts under whichever integration is chosen |
| MCP server's conversation history | Replayed into each subprocess call | Must keep working under the 2.x API |

## Testing approach

Unit tests with a mock model stay green, plus new cases for refusals and timeouts. The MCP server's `pytest` suite is ported to 2.x. Live checks with a real API key confirm that Sonnet 5.5 calls the tools on all four bundled datasets at the chosen effort. They also record time and cost per question, so effort is chosen by measurement. Manual Claude Desktop checks go in `VMR_MODERNIZE_TESTING.md`.

## Implementation sequence

1. Decide the integration (open issue 1).
2. Agent: integration, effort, thinking blocks, refusals, timeouts.
3. System prompt audit and rewrite, checked live on all four datasets.
4. MCP server on 2.x.
5. Docker base, docs, and release.

## Scope boundary — what this does NOT include

- New tools, new analysis features, or changes to the two-module architecture.
- Support for non-Claude models.
- The Trino upgrade and default-model swap, which are `VMR_TRINO_483`.

## Open issues

1. Stay on LangChain4j (upgraded to 1.22) or move to the official Anthropic Java SDK. As of 1.22, LangChain4j handles thinking blocks (`returnThinking`/`sendThinking`) and an explicit `maxTokens`. It has no effort setting or refusal handling. Effort could only be sent through its `customParameters` map, untested and possibly colliding with its own `output_config`. Weigh that against rebuilding the mock-model test seam on the official SDK.
2. Which effort level for Sonnet 5.5. Its default is `high`; start the measurement at `medium` for multistep tool use.
3. Timeout values for the agent and the MCP subprocess, and whether a long question should report progress rather than just wait.
