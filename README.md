# virtual-view-brain 🧠

This [mini-brain](https://github.com/robfromboulder/mini-brain-toolkit) allows all virtual view knowledge and history to be used from any Claude session, and provides standard workflows to maintain and improve this knowledge over time.

It covers the three projects that define, implement and support the virtual view pattern on Trino: [virtual-view-manifesto](https://github.com/robfromboulder/virtual-view-manifesto), [viewmapper](https://github.com/robfromboulder/viewmapper) and [viewzoo](https://github.com/robfromboulder/viewzoo).

This is not a "second brain" with the goal of capturing all virtual view knowledge -- this mini-brain only maintains information that cannot be derived from the codebases.

## Knowledge files

All knowledge is stored in Markdown files. Each file captures an orthogonal dimension of knowledge: its scope, technical approach, work in progress, session history, and so on.

Knowledge is divided into lobes, because the three projects hold three different problems. Each lobe has its own directory and its own lobespace, and the hub at the repo root holds what spans them:

| Lobe | Directory | Lobespace |
|---|---|---|
| Hub -- the ecosystem as a whole | `.` | `VV` |
| Manifesto | `manifesto/` | `VVM` |
| ViewMapper | `viewmapper/` | `VMR` |
| -- Agent | `viewmapper/agent/` | `VMR_AGENT` |
| -- MCP server | `viewmapper/mcp/` | `VMR_MCP` |
| ViewZoo | `viewzoo/` | `VZOO` |

CLAUDE.md provides the read index, so that Claude can discover and apply knowledge that is relevant to the active chat session. It resolves a lobe's files from a doctype grammar and the registry above rather than listing every file.

Lobespaces let you load more than one mini-brain into the same coding session without filename collisions or confusion during updates.

## Usage

#### 1. Use virtual view knowledge from a sibling repo directory:

> Read ../virtual-view-brain/CLAUDE for instructions

From the ViewMapper submodules, which sit one level deeper:

> Read ../../virtual-view-brain/CLAUDE for instructions

#### 2. Save notes about this Claude session:

> Read VV_SESSION_CLOSEOUT and append to the right log
