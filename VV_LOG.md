# Virtual View: Session Log

Running log of Virtual View implementation sessions. Each session appends after a `---` separator. Read only from the last `---` separator forward — this file grows large.

---

# Brain seeded from plan through repo trim, with the scopes rewritten once (2026-08-02)

**Session ID**: `e054f1be-03ab-4b37-a0dd-74f68fd3df60`

Rob's session, with Claude as co-author. It opened on his feedback against the five open decisions in the bootstrap plan and ran through the seeding sequence to the end of the repo trim: tree and 27 files, entrypoint, source material archived, README replaced, all twelve scope and approach documents authored, hooks added to the project repos, and the project repos trimmed. Steps 1–6, 10 and 11 are complete; step 7 is partial and 8, 9 and 12 remain. The scopes were authored once, found to be wrong in kind rather than in detail, and rewritten. Nothing committed in any of the four repos.

## Turn-by-turn

- Rob settled all five open plan decisions in one pass. The hub scope became a short problem statement naming the theme rather than a summary of the component scopes; security guides were deferred with no work items rather than seeded as empty shells; `ARCHITECTURE.md` was to leave nothing behind, with its knowledge going to the brain and its runbook half to a new root entrypoint; the manifesto's agentic ambitions were held to what is true today; and its TODO list became one work item carrying the thematic grouping in its plan rather than three to five items guessed in advance.
- Seeding through the entrypoint, archive and README was uneventful. Archiving the source material first turned out to matter later — it is the only reason deleting the largest source document was reversible.
- The hub scope and approach were authored, then each component's, parents before children. The first pass looked finished and was not: Rob read the scopes back and identified that every "current state" section described the maturity of the thing being built rather than the world the problem lives in, and that several goals were design commitments in disguise. All six were rewritten. Version numbers, test counts, benchmarks and issue counts came out; what the platform provides and withholds, what alternatives exist, who has the problem and what evidence there is went in.
- Rob then ran two review cycles. Reading the six scopes as a group found nine issues that no single-document reading would surface — a term carrying two meanings across units, an open question standing in both a parent and a child, the hub explaining a child's problem rather than naming it, and an assumption about where the reader works that had leaked into a scope from a design decision made two documents downstream. Pairing each approach with its own scope, and deliberately not with the other approaches, found a factual contradiction between hub and child plus three goals with no answering decision.
- The corrections were fed back into the toolkit as a separate closeout.
- Adding the hooks turned up a plan error: the two ViewMapper modules are directories inside one repo, not repositories of their own, so the sequence covers three hooks and not five. The modules took a component anchor pointing at the new root entrypoint instead of a second copy of the hook.
- The trim uncovered a sequencing dependency the plan does not state. Deleting `ARCHITECTURE.md` and the modules' design-decision sections would have destroyed rejected paths and non-obvious limitations that no approach document had captured, because the findings step had been skipped. The agent and MCP findings were written first, then the deletions ran.
- Reading the entrypoint files back in topological order found the brain's own `CLAUDE.md` still carrying the terminology every scope had moved away from, and a reference in all three project hooks to mini-brain commit conventions that the brain had never stated. Rob extended the commit conventions to the three project repos as well.

## Corrections against the code

- The plan claimed the two code projects were at different Trino versions. Both are on 479 with JDK 25, committed.
- ViewMapper's open issue asking to branch and update for Trino 479 is asking for work that already shipped; what remains of it is a request to change the release strategy, which is different work.
- The manifesto's own instructions claimed eight use cases with the eighth a stub. There are seven.
- The manifesto is CC0, not Apache 2 like the two code projects. An earlier draft of the hub approach had them all under one license.
- ViewMapper's contribution guide told contributors to keep line-number references synchronized and, in the same file, forbade line numbers in documentation. The instruction to maintain them is gone.

## Decisions

- **Defer rather than pre-seed** — the two security-guide issues get work items when someone picks one up, because an unstarted item makes the in-flight area look busier than the work is (Rob).
- **Delete the architecture document outright** — a stub landing page is exactly what the new root entrypoint already is, and two files doing that job drift apart (Rob).
- **Scopes are read as a group; approaches never are** — an approach is judged against its own problem, not against how its siblings look (Rob).
- **Capture findings before deleting their source** — the trim step cannot run ahead of the findings step for any document about to be removed (Claude).
- **State commit conventions where they are referenced** — three hooks pointed at conventions that did not exist; the brain now states them and the project repos carry the same rule for their own commits (Claude's finding, Rob's call to extend it).

## What didn't work

- Authoring the scopes from the project repositories' own documentation reproduced the shape of that documentation. Every scope came out as a status report, and the error was uniform enough to rule out carelessness in any one document.
- The assumption that ViewMapper's users work in a chat client was written into its scope as a fact about the world. It is a consequence of the delivery decision recorded two documents away, and it read as description rather than as design because of where it landed. Removed; the module whose problem genuinely is the destination keeps it.
- An unfounded causal claim survived into the hub scope: a source recorded that a team maintains their own view-storage module and wanted to migrate off it, and the distillation asserted why they had built it. Sources record what was done far more often than why.

---

# Add work setup and closeout procedures, retire bootstrap plan (2026-08-10)

**Session ID**: `98b66627-3479-4d82-9fc0-3261108d235f`

Rob's session, with Claude as co-author. Added `VV_WORK_SETUP.md` and `VV_WORK_CLOSEOUT.md` to the hub — the brain's first work-item machinery — adapted from the mini-brain toolkit's templates. Retired `VV_BOOTSTRAP_PLAN.md` to `archive/` and updated the hub index.

## Turn-by-turn

- Rob asked whether the work setup and closeout procedures should live at the leaves (one per component) or at the hub. Claude read the toolkit's `MBT_COMPONENTS.md`, which states that maintenance and procedure documents live at the hub — one of each serves every unit and none is namespaced to a component. The working docs those procedures scaffold land in whichever unit owns the work item. Rob confirmed.
- Claude read both toolkit templates (`WORK_SETUP.md`, `WORK_CLOSEOUT.md`) and all six base work templates (`PLAN.md`, `FINDINGS.md`, `LOG.md`, `BURNDOWN.md`, `CLAUDE.md`, `TESTING.md`), then drafted both procedures with the `VV` prefix and the six templates inlined into WORK_SETUP so the brain stands alone without the toolkit.
- The owning-unit derivation in the intake step was adapted for a component brain: it points at the registry's Routes on column and walks up to the nearest common ancestor. The toolkit has an open work item to strengthen this step further; the current version was used as-is.
- Rob noted the bootstrap plan was fully complete and asked to retire it. Moved to `archive/` and its row removed from the hub documents table.
- `CLAUDE.md` bumped to V4: two rows added for the new procedures, one row removed for the retired plan.

## Decisions

- **One procedure set at the hub, not per-leaf** — the toolkit is explicit that maintenance documents serve the whole brain; per-component copies would duplicate the placement logic and need syncing (Rob confirmed Claude's reading of the toolkit).
