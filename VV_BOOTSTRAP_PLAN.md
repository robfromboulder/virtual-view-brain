# Virtual View Brain: Bootstrap Plan

> V1, 2026-07-31.

The plan for seeding this brain: what it holds, where each piece of existing knowledge lands, and the order to do it in. This is a planning document, not a canonical one — retire it to `archive/` once the seed is filled.

---

## 1. What this brain holds

The virtual view ecosystem: three projects that define, implement and support the virtual view pattern on Trino. Trino is the only platform. Starburst Enterprise and Galaxy are mentioned as compatible but are not documented, tested or supported, and nothing about them belongs in this brain.

Five units, because five distinct problems compose:

| Unit | Problem it owns |
|---|---|
| **Hub** | Why virtual views need a pattern, a store and a mapper at all, and how the three fit together. |
| **Manifesto** | Getting the virtual view pattern understood and applied. Its output is prose, not code. |
| **ViewMapper** | Understanding sprawling view hierarchies on Trino — and how its two modules compose to do that. |
| **— Agent** | Analyzing Trino schemas and view dependency graphs at scale. |
| **— MCP server** | Making that analysis usable conversationally, which is where session context, subprocess lifecycle and diagram rendering live. |
| **ViewZoo** | Storing views for Trino without a heavyweight metastore. |

The agent and the MCP server are separate units rather than one because their problems differ, not because their stacks do. Issue traffic confirms it: "identify isolated views" is pure graph analysis and touches nothing conversational, while "better hinting that mermaid diagrams should be treated as files" is pure chat-client behaviour and touches nothing analytical.

---

## 2. Layout

```
CLAUDE.md              # entrypoint: hub index, doctype grammar, component registry
README.md
VV_SCOPE.md  VV_APPROACH.md  VV_FINDINGS.md  VV_LOG.md  VV_SESSION_CLOSEOUT.md
manifesto/             VVM_SCOPE.md  VVM_APPROACH.md  VVM_FINDINGS.md  VVM_LOG.md
viewmapper/            VMR_SCOPE.md  VMR_APPROACH.md  VMR_FINDINGS.md  VMR_LOG.md
  agent/               VMR_AGENT_SCOPE.md  VMR_AGENT_APPROACH.md
                       VMR_AGENT_FINDINGS.md  VMR_AGENT_LOG.md
  mcp/                 VMR_MCP_SCOPE.md  VMR_MCP_APPROACH.md
                       VMR_MCP_FINDINGS.md  VMR_MCP_LOG.md
viewzoo/               VZOO_SCOPE.md  VZOO_APPROACH.md  VZOO_FINDINGS.md  VZOO_LOG.md
archive/  working/     # hub-level; each unit grows its own when it first needs one
```

Twenty-seven files at seed. Session closeout is the brain's single maintenance document and stays at the hub; so will work setup, work closeout and the dream cycle when they arrive.

Registry to write into `CLAUDE.md`:

| Component | Directory | Token | Routes on | Also holds | Project repo |
|---|---|---|---|---|---|
| Manifesto | `manifesto/` | `VVM` | manifesto, book, chapter, section, use case, anti-pattern, editorial, voice | — | `../virtual-view-manifesto` |
| ViewMapper | `viewmapper/` | `VMR` | viewmapper, schema exploration, lineage, dependency graph, release, versioning | — | `../viewmapper` |
| — Agent | `viewmapper/agent/` | `VMR_AGENT` | agent, CLI, JDBC, Trino parser, JGraphT, LangChain4j, catalog discovery | — | `../viewmapper/viewmapper-agent` |
| — MCP server | `viewmapper/mcp/` | `VMR_MCP` | mcp, Claude Desktop, session context, subprocess, mermaid rendering | — | `../viewmapper/viewmapper-mcp-server` |
| ViewZoo | `viewzoo/` | `VZOO` | viewzoo, view storage, connector, JDBC storage, caching, multi-tenancy, branch | — | `../viewzoo` |

`viewmapper/` holds what spans its two modules and is where cross-module work logs. The hub holds what spans the three projects.

---

## 3. Content mapping

"Distill" means the un-derivable decision and its reasoning move; the derivable detail stays where it is. Nothing from the manifesto's own chapters is restated here — that repo is ground truth for its own content.

### Moves into the brain

| Source | Lands in | What moves |
|---|---|---|
| manifesto `CLAUDE.md` — overview, success criteria, target audience | `VVM_SCOPE.md` | Problem, audience, what success looks like |
| manifesto `CLAUDE.md` — voice and tone, terminology table, use-case selection criteria | `VVM_APPROACH.md` | Editorial strategy and the conventions that can't be read off the text |
| manifesto `CHANGES.md` (103 lines, v0.4–v0.69) | `VVM_LOG.md` | One historical-context entry summarizing the arc — not a per-version translation |
| viewmapper `ARCHITECTURE.md` — value proposition, what the project is for | `VMR_SCOPE.md` | Problem statement |
| viewmapper `ARCHITECTURE.md` — version numbering rationale, positioning and interview framing | `VMR_APPROACH.md` | How the author wants the project understood; release conventions |
| viewmapper `CONTRIBUTING.md` — the "Claude Code required" model | `VMR_APPROACH.md` | Architecture-first development as a strategic choice; the operational steps stay put |
| viewmapper `ARCHITECTURE.md` — how the MCP server drives the agent (JAR, subprocess) | `VMR_APPROACH.md` | The composition of the two modules — interfaces and why, never either one's internals |
| viewmapper `ARCHITECTURE.md` + agent `CLAUDE.md` — Java CLI over microservice, multi-catalog-first JDBC, discovery-is-essential | `VMR_AGENT_APPROACH.md` | The agent's design and the alternatives weighed |
| viewmapper `ARCHITECTURE.md` — system prompt strategy, agent reasoning flow | `VMR_AGENT_APPROACH.md` | The intent behind the prompt, not the prompt text |
| agent `CLAUDE.md` — design decisions | `VMR_AGENT_FINDINGS.md` | Why the Trino parser over regex, why JGraphT, why `DefaultDirectedGraph`, why LangChain4j |
| viewmapper `ARCHITECTURE.md` — removed designs (`SchemaExplorationService`, `ExplorationResult`, `ExplorationContext`) and why | `VMR_AGENT_FINDINGS.md` | Rejected paths, invisible from current code |
| mcp `CLAUDE.md` — design decisions | `VMR_MCP_FINDINGS.md` | Why prompt-based context, why a 3-turn window, why a 60s timeout |
| mcp `CLAUDE.md` — what the conversational surface has to be | `VMR_MCP_APPROACH.md` | Why the server is thin and stateless-ish, and what that costs |
| viewzoo `CLAUDE.md` — architecture and key patterns | `VZOO_APPROACH.md` + `VZOO_FINDINGS.md` | Provider pattern rationale, synchronized access, caching strategy |
| viewzoo — per-Trino-version branch strategy | `VZOO_FINDINGS.md` | Why branches per version rather than one trunk |
| All three READMEs, plus how the projects reference each other | `VV_SCOPE.md`, `VV_APPROACH.md` | Why the three exist as one system and how they compose |

### Stays in the project repos

READMEs (user-facing, unchanged), every `CONTRIBUTING.md`, both `TESTING.md` files, `.gitignore` and `LICENSE`, and the operational half of each `CLAUDE.md`: build and test commands, configuration, run instructions, code style, test-dataset descriptions, the manifesto's section-file format and build workflow, and its "Requesting Critical Reviews" persona — a runbook behaviour, not knowledge about the manifesto.

### Trimmed after the brain absorbs it

| File | What goes | What replaces it |
|---|---|---|
| manifesto `CLAUDE.md` | Success criteria, target audience, project overview | A pointer to the brain for strategic context |
| manifesto `TODOS.md` (48 lines) | Nothing yet — mark items as imported, remove once work items exist | — |
| manifesto `CHANGES.md` | Nothing; it is the public changelog and should diverge from the brain's log | — |
| viewmapper `ARCHITECTURE.md` (875 lines) | Most of it. Rationale, rejected alternatives, prompt strategy, versioning and positioning all move; the rest (tech stack, project structure, code samples, build scripts, config examples, algorithm walk-throughs) is re-derivable from source and the submodule runbooks | Full file copied to `archive/` as source material. Decide whether the repo keeps a short stub — see §6 |
| agent `CLAUDE.md` | Design decisions, known limitations | A pointer to the brain |
| mcp `CLAUDE.md` | Design decisions | A pointer to the brain |
| viewzoo `CLAUDE.md` (92 lines) | The rationale under key patterns; the pattern names stay | A pointer to the brain |

Note that `../viewmapper` has no `CLAUDE.md` at all. Its hook creates one.

---

## 4. Work items

Work items live in the `working/` of the unit that owns them, named `<TOKEN>_<WORK>_*`.

### ViewMapper — 8 open, 1 closed

| # | Title | Owner | Work item |
|---|---|---|---|
| 1 | Branch and update for Trino 479 | `viewmapper/` | `VMR_TRINO_479_UPGRADE` — also carries the JDK 25 move |
| 2 | Test/document examples with user authentication enabled | `viewmapper/` | `VMR_AUTH_TESTING` |
| 3 | Is `exclude_columns` supported? | agent | triage — answer likely becomes a findings entry |
| 4 | Add security guide | `viewmapper/` | `VMR_SECURITY_GUIDE` — pairs with ViewZoo #11, see §6 |
| 5 | Notebooks or other interactive renderings? | agent | triage — park as an open question in `VMR_AGENT_SCOPE.md` |
| 6 | Identify isolated views (no base or dependents) | agent | `VMR_AGENT_ISOLATED_VIEWS` |
| 7 | Better hinting that mermaid diagrams are files | mcp | triage — Claude Desktop behaviour, may not be actionable |
| 8 | Improve error handling if agent can't connect | mcp | `VMR_MCP_CONNECTION_ERRORS` |
| 9 | Prompts against test datasets aren't working | — | closed |

Five actionable, three to triage. The three that span both modules (#1, #2, #4) sit in `viewmapper/working/`; the module-specific ones sit in their own module's.

### ViewZoo — 6 open, 7 closed

| # | Title | Work item |
|---|---|---|
| 9 | Test cases should include renaming views | `VZOO_RENAME_TESTS` |
| 10 | Improvements for multi-tenancy | `VZOO_MULTI_TENANCY` — hardcoded table name, multi-instance docs, perf testing |
| 11 | Add security guide | `VZOO_SECURITY_GUIDE` — see §6 |
| 12 | Offer versioned binaries | `VZOO_VERSIONED_BINARIES` |
| 13 | Configurable VIEW security mode | `VZOO_SECURITY_MODE` — community request; design discussion first |
| 14 | Configurable caching | `VZOO_CONFIGURABLE_CACHE` — community request; design discussion first |

All six sit in `viewzoo/working/`. Issues #13 and #14 carry use-case context from their requesters that exists nowhere but the GitHub thread — capture it when the work item opens.

Closed ViewZoo #8 was the Trino 479 branch, so ViewZoo is already on 479 while ViewMapper #1 is still open. The two projects are at different Trino versions right now, and work items should say which version they target.

### Manifesto — no issues

Work comes from `TODOS.md` instead: roughly twenty items ranging from one-line questions to multi-paragraph proposals. Group into three to five thematic items rather than twenty micro-items, with each item's task list carrying the individual TODOs.

---

## 5. Seeding sequence

1. **Create the tree and seed all 27 files.** Skeletons with version headers; hub `archive/` and `working/` only.
2. **Write `CLAUDE.md`** from the component entrypoint template: hub index, doctype grammar, the registry in §2, and the conventions.
3. **Copy source material to `archive/`** — viewmapper `ARCHITECTURE.md` above all, since most of it is about to be absorbed.
4. **Replace `README.md`.** It currently holds the original prompt for this repo; it should say what the brain is and how to load it.
5. **Fill `VV_SCOPE.md`, then `VV_APPROACH.md`.** Parents settle before children, and problems before designs.
6. **Fill each component's SCOPE, then its APPROACH** — `viewmapper/` before `agent/` and `mcp/`.
7. **Seed the FINDINGS documents** from the design decisions in §3.
8. **Seed `VVM_LOG.md`** with the historical-context entry drawn from `CHANGES.md`.
9. **Fact-check every falsifiable claim against the code.** Scopes distilled from project docs drift in predictable ways — they overstate uniformity, mislabel by name, and lag the code. Correct what the code contradicts and bump versions.
10. **Add the hook to five repos** — `virtual-view-manifesto`, `viewmapper` (creating its `CLAUDE.md`), `viewmapper-agent`, `viewmapper-mcp-server`, `viewzoo` — each naming its own component.
11. **Trim the project repos** per §3, leaving pointers.
12. **Verify the round trip** from each repo: load the brain, confirm the registry routes correctly, and confirm a session lands in the right unit without reading the others.

Steps 1–4 are one session's work. Steps 5–9 are the substance and will take several. Work-item import comes after, once the shape has been used in anger.

---

## 6. Decisions still open

**Does `VV_SCOPE.md` say anything the component scopes don't?** Its APPROACH clearly does — how a manifesto, a store and a mapper compose is real un-derivable knowledge. The SCOPE is the doubtful half. Write it and see; if it turns out to be a summary of the other four, cut it back to a short problem statement and let the APPROACH carry the weight.

**One security guide or two?** ViewMapper #4 and ViewZoo #11 are the same request against different projects. Two separate work items keep each in its owning unit; a single `VV_SECURITY_GUIDES` item at the hub coordinates delivery but puts implementation work above the units that will do it. Prefer two unless they genuinely ship together.

**Does `ARCHITECTURE.md` leave a stub behind?** The full file is archived either way. The question is whether `../viewmapper` keeps a short landing page pointing at the submodule runbooks and the brain, or whether the new root `CLAUDE.md` created by the hook covers that need on its own. The second is tidier if the hook's file ends up carrying an overview anyway.

**How agentic does the manifesto become?** The intent is to grow a cookbook from the same material — knowledge applied through an interface rather than absorbed by a reader. That cookbook is a deliverable of the manifesto repository, not a brain document; the brain holds why it says what it says. Settling this changes what `VVM_SCOPE.md` claims, so decide before filling it.

**How granular are the manifesto work items?** Three to five thematic groups is the working assumption. The grouping is easier to judge once `VVM_APPROACH.md` states the editorial strategy, so import after that, not before.
