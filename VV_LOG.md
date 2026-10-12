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

---

# Brain checked against the toolkit, and every finding worked through (2026-09-23)

**Session ID**: `2194a995-5785-4dd5-937b-e439c296639b`

Rob's session, with Claude as co-author. It ran the mini-brain toolkit's brain check (`MBT_CHECK_BRAIN.md`) against this brain, then walked through each recommendation in turn. The brain came out healthy — structure clean, scopes describing the world rather than project status, and nearly every falsifiable claim holding against the code — and the session fixed what the check did find: a mistaken work item deleted, the retired bootstrap plan's loose ends settled, two parent scopes trimmed back to naming their children, the brain's vocabulary moved to lobe and lobespace, the entrypoint tidied, and two small factual and pruning fixes.

## Turn-by-turn

- Claude read the check procedure with the toolkit's pattern and multi-lobe references, then the whole brain directly — small enough that delegating the reads would have cost more than it saved — and checked claims against the three project repos and their GitHub issues. The claims held: the manifesto's ten section files, the agent's six tools, the MCP server's sixty-second deadline and three-turn history, ViewZoo's `READ_COMMITTED` declaration and synchronized metadata, the licensing split, the Starburst disclaimer in every repo, neither tool linking back to the manifesto, `479a`-style release tags, and nothing exercising `exclude_columns`. The one drift was the hub approach describing ViewZoo's branches as a continuous v470–v479 range, when v471–v474 do not exist.
- The check's sharpest finding was `VMR_TRINO_479`, which planned to branch ViewMapper per Trino version and share a branching schedule with ViewZoo — the reverse of the hub approach's deliberate release-strategy split, for an upgrade already on ViewMapper's `main` and tagged `v479a`, and without naming the decision it would reverse. Rob identified it as a mistake: he had found it uncommitted locally and taken it for something a previous session had neglected to commit. It was deleted rather than archived, since it never started. `VZOO_TEST_VIEW_RENAMING` arrived in the same commit and was kept once it was confirmed to match an open ViewZoo issue.
- The retired bootstrap plan still ended with the rest of its findings step, the manifesto log seeding, the fact-check and the round-trip verification outstanding, while this log recorded it as fully complete. Rob settled each one.
- Parent overreach was the main substance issue. The hub scope's state-of-the-problem section carried three subsections restating the manifesto's, ViewMapper's and ViewZoo's scopes nearly word for word, and ViewMapper's scope explained the SQL-parsing failure modes, the structural questions and the cold-start problem that the agent's scope owns. Each passage was checked against the child before it was cut; every one was already there, usually in more detail, so nothing needed adding below.
- The vocabulary rename replaced "unit", "component", "token" and `<TOKEN>` with lobe and lobespace across `CLAUDE.md`, `README.md` and the three procedures. A plain word swap misread two sentences where "component" had meant a child, since the hub is itself a lobe, and those were fixed by hand. Ordinary uses ("unit vs. integration", "every token is load-bearing") were kept, and earlier log entries were left as written.
- The entrypoint tidy removed commented index rows for procedures that were already live, activated the maintenance-doc boundaries rule for the procedures that exist, corrected the version exemption to the burndown checklists the brain actually uses, and narrowed routing terms that pulled questions to the wrong lobe: bare "agent" (the manifesto discusses agent readers), "release, versioning" (the strategy is a hub decision spanning both code projects), bare "JDBC" (claimed by both the agent and ViewZoo's storage) and bare "branch" (which matched work-item branches).
- The last fixes dropped the branch range from the hub approach, and cut ViewZoo's architecture description to how its parts compose, removing framework wiring the code already shows.

## Decisions

- **Delete `VMR_TRINO_479` as a mistake** — it was committed by accident, duplicated shipped work, and contradicted the hub's release strategy (Rob).
- **Keep `VZOO_TEST_VIEW_RENAMING`** — real work matching an open issue (Rob).
- **Seeding the manifesto log from its changelog is deferred** to a later manifesto session (Rob).
- **The bootstrap fact-check counts as done by this check** (Rob, on Claude's recommendation).
- **Round-trip verification is dropped** — real sessions from the hooked repos exercise routing (Rob).
- **The eight planned work items never created open when someone picks one up**; GitHub issues and the manifesto's TODO list stay the backlog, extending the earlier defer-rather-than-pre-seed decision (Rob, on Claude's recommendation).
- **Work items' manual test checks and runbook steps fold into the owning project repo's `CLAUDE.md` at closeout**, never into the brain — they are operational and live beside the code (Rob).
- **The open question on whether guidance suffices where the engine will not help stays at the hub** — if it does not, the remedy may be a tool, and which project provides it is a hub decision (Rob).
- **Drop enumerated branch ranges rather than correct them** — git shows them, and a list goes stale with every Trino release (Claude).

## Lessons

- A work item that arrives without its intake conversation needs checking against the canonical decisions before it is trusted. This one read as routine and contradicted the hub approach.
- The toolkit's vocabulary rename cannot be a pure word swap in a multi-lobe brain: "component" often meant *child*, and the hub is a lobe too.

---

# Manifesto comic shipped, and only the opening sheet is drawn (2026-10-12)

**Session ID**: `409efda1-fdc5-4f1a-9935-363ff19c2e3b`

Rob's session, with Claude as co-author. It set out to turn the multi-panel comic prototype into the real opening of the manifesto README, with a list of changes from Rob, and left the prototype untouched. After many rounds of review, the comic shipped with badges in manifesto v0.70, tagged and pushed. Along the way Rob decided that the opening sheet is the only drawn part of any README, and the visual design doc and the design system were brought into line with that.

## Turn-by-turn

- Claude read the visual design doc, the design system's README and the prototype, then built `m000-manifesto.src.svg` from the prototype's splash and phasing row. Rob's first list of changes:
  - Drop the sheet-code line and the section line.
  - Reword the subheadline to "use them as data contracts for apps and agents".
  - Replace the principles, use cases and pitfalls counts and the CC0 note with the eight principles.
  - Light the candle as on the brain README's manifesto tile.
  - Make "query running from the application" the cake's only yellow text.
  - Make the column-types note white, and mark the shaded part of each tier as test data.
  - Retitle phase 2 as a zero-downtime migration with a "swap in new version" note.
  - Retitle phase 3 as an Iceberg scale-out with a new storage tier under PostgreSQL.
- No fonts were on disk for `text2path.py`. Claude downloaded them from google/fonts into the session scratchpad, instanced Caveat at 700, and checked each export by rendering it to PNG with `qlmanage`.
- Rob iterated on the layout over many rounds:
  - The splash lost its frame.
  - The principles gained a dimension mark, labelled "8 organizing principles".
  - The subheadlines were matched in size and color, and the left column was moved down.
  - The test-data label went from a legend to an arrowed note pointing at the bottom tier.
  - The versioned layer and base views each got a "replaceable layer" dimension mark.
  - The yellow notes in all three phases moved to the left side, pointing at the layer that changed and away from the shaded test data.
  - Phase 2 put `orders_v2` in the center slot, with `orders_v1` floating out.
  - Panel 1 became "view hierarchy in service", with "stable views as data contract" pointing at `myapp.*`, since the splash already explains the candle.
  - The Trino footer line went, and the tagline became "no one changed the app", with an arrow to panel 1.
  - The title block became version, scale, revision date and license.
  - The wording of several principles was changed.
- Rob asked whether the manifesto's Mermaid diagrams should be redrawn as blueprint SVGs. Claude advised keeping Mermaid. Agents read Mermaid source as text, but the export outlines all lettering, so an SVG gives an agent only its alt text. Claude suggested themed Mermaid as the cheap path if polish matters later. Rob made this a standing decision, and observed that the viewzoo and viewmapper READMEs already conformed.
- Claude updated the visual design doc, then, with Rob's approval, the design system:
  - The ChapterSheet component and its two type styles were removed.
  - The ComicPage card and preview now show the shipped comic.
  - The ReadmeLayout and TitleBlock cards and previews now match the shipped READMEs and title blocks.
  - The cast's cake and the title-block guidance were updated.
  - Rob had the doc point only at the design system.
- Adding badges exposed that the manifesto's README is generated from `sections/` by `build.sh`, as its `CLAUDE.md` says. Every edit made to `README.md` so far would have been lost at the next build. That included Rob's own removal of the Caution alert, made before the session. All of it moved into `sections/00-header.md`, and a rebuild produced the same README plus the badges.
- Rob bumped the manifesto to 0.70 in the footer section, and the comic's title block followed. The manifesto was committed, tagged `v0.70` and pushed. The visual design doc was committed and pushed separately, after Claude read it back and fixed three wordings.

## Decisions

- **Only the opening sheet is drawn.** A hero opens each tool README and the comic opens the manifesto. Everything after it is portable markdown with `##` headings and Mermaid diagrams. The chapter sheets once proposed for section headings are retired (Rob, on Claude's recommendation about agent readability).
- **The visual design doc points only at the design system.** The chapter-sheet, blueprints and comic-prototype pages show retired designs, so they are no longer linked. The shipped READMEs are the worked examples (Rob).
- **A label centered in a cake tier may cross a major grid line** when moving it off would crowd the tier (Rob, prompted by the `postgresql.myapp.*` label).
- **The comic's title block carries version, scale, revision date and license**, and the version and date follow the manifesto's footer. "Scale: enterprise" is a deliberate joke on a field that normally holds a ratio (Rob).
- **The comic's checker notes sit on the left of each phase**, pointing at the part that changed and clear of the shaded test data (Rob).
- **Manifesto 0.70 is tagged `v0.70`**, as a lightweight tag like earlier releases (Rob).

## What didn't work

- **Editing the generated README directly.** Claude never checked the manifesto repo's own instructions before editing `README.md`. The mistake surfaced only when badges were added, and it would have silently reverted Rob's Caution-alert removal too.
- **Hand arithmetic for grid-line clearance.** Claude twice told Rob that the principles list could not move lower without a line hitting a major grid line, and both claims were wrong. A brute-force search over start positions and spacings found valid placements right away.

## Lessons

- Read a project repo's `CLAUDE.md` before editing anything in it. A generated file looks like source until its build runs.
- Check grid-line clearance by computing it: cap height from the font, then every baseline checked against the 100px grid.
- Three open questions came out of the work: whether PhasingSheet still earns its place as a standalone component, the shipped heroes' 10px title-block field names against the 12px minimum, and the stale HeroSheet, IndexSheet and PhasingSheet previews. They are recorded in the visual design doc.
