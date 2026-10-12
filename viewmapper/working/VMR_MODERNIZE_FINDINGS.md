# Modernize: Decision Record

## Problem

ViewMapper's Claude integration and MCP server were written for the models and SDKs of late 2025, and nothing has been updated since. The Trino 483 upgrade replaces the retired default model with Sonnet 5.5, but only as far as needed to make it work. The rest still assumes an older generation:

- **No control over effort** — current models always think, and effort is the only lever on how much.
- **No refusal handling** — current models can end a turn with `stop_reason: "refusal"`.
- **Timeouts sized for models that didn't think** — 60 seconds in the agent and 60 in the MCP server's subprocess call.
- **A system prompt written for Sonnet 3.7.** Prompts written for older models tend to be too prescriptive for current ones and can lower answer quality.
- **Old dependencies** — LangChain4j 1.10 (1.22 is current), and the MCP Python SDK pinned below 2 (2.3 is current). Even 1.22's Anthropic model has no effort setting and no refusal handling: its `output_config` carries only a response format.
- **An unpinned first Docker stage** on Ubuntu 22.04.

## Preferred approach: modernize in place, keeping the architecture

Keep the two-module design, the subprocess interface, and the six tools. Bring each layer up to current practice:

| Aspect | Detail |
|---|---|
| Claude integration | LangChain4j 1.22, or the official Anthropic Java SDK (`anthropic-java`) with its tool runner — decided in this item |
| Effort | Set explicitly and chosen by measurement on the bundled datasets, rather than left at the default |
| Thinking | Thinking blocks are returned unchanged with each tool result, as current models require |
| Refusals | `stop_reason: "refusal"` is handled and reported to the user, with server-side fallback enabled where the integration supports it |
| Timeouts | Agent and MCP subprocess timeouts sized for thinking models, and kept consistent with each other |
| System prompt | Audited for patterns written for older models, then trimmed, not ported line for line |
| MCP server | MCP Python SDK 2.x. Its low-level `Server` and `stdio_server`, which `mcp_server.py` uses, are still in 2.3.0, so the port may be small |
| Image | A pinned, current Ubuntu base for both Docker stages |

- **Same shape, current parts** — the design decisions in the ViewMapper approach docs still hold. What has aged is the dependencies and the assumptions built into the prompt and the settings.
- **The default model stays a Sonnet** — Sonnet 5.5, already set by the Trino 483 upgrade, at half Opus 5.5's per-token price for users paying with their own API key.

## Alternatives considered

- **Stop at the model swap** — `483a` works with Sonnet 5.5 and LangChain4j 1.10, but without effort control, refusal handling or a prompt written for the model it runs on.
- **Default to Opus 5.5** — Anthropic's current default model, but twice the per-token price. `ANTHROPIC_MODEL` still lets users choose it.

## What this doesn't solve

- Cheaper models still need checking for whether they actually call tools before anyone recommends them.
- Answers remain an aid that needs review by someone qualified, not an authority.

## Reversals

- `VMR_AGENT_APPROACH.md`, Key Design Decisions — "LangChain4j for the model integration." It is reversed only if this item chooses the official SDK.
