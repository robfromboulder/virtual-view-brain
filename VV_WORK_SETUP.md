# Virtual View: Work Setup

> V3, 2026-09-23.

Procedure for scaffolding a new work item's working docs from an intake conversation. The bookend to `VV_WORK_CLOSEOUT.md`: setup creates the `working/` docs at branch start, closeout folds them into the canonical mini-brain when the work concludes. Read `CLAUDE.md` first for file conventions — they govern every file this procedure touches.

Run this when starting a new work item — **code-changing work that gets its own branch and PR**: a feature, a bug fix, or a hardening effort — or when formalizing a partial one that already lives in `working/` (e.g. a PLAN+FINDINGS pair that needs the rest of its scaffolding). The output is the `working/<LOBESPACE>_<WORK>_*.md` documents that track a work item until it concludes. `<LOBESPACE>` throughout is the owning lobe's lobespace — resolved from the lobe registry in `CLAUDE.md`. Setup is **additive and idempotent**: it creates only the docs that are missing and never overwrites existing work, so it is safe to re-run as a work item grows.

The scope is deliberately narrow and practical: **assume a work item has a branch and a PR until proven otherwise.** It is often not knowable at inception whether an idea is a shallow doc/config tweak or something deeper, so default to the full scaffold rather than guessing small — an oversized scaffold is cheap, and under-scaffolding something that turns out deep is not. If the work later concludes without a merge, closeout still folds in whatever knowledge the docs hold (see `VV_WORK_CLOSEOUT.md`) rather than being forced through the burndown. A pure question that produces no artifact worth keeping needs no work item at all: answer it, and if the answer is worth recording, add a session-log entry.

The working docs and their roles:

| Doc | Role | Seeded at setup from the chat? |
|---|---|---|
| `<LOBESPACE>_<WORK>_PLAN.md` | The spec: objective, what changes, testing approach, scope boundary, open issues. A frozen input to code generation — often archived as soon as its code is generated | Yes — written from the intake conversation |
| `<LOBESPACE>_<WORK>_FINDINGS.md` | The decision record: problem, preferred approach, tradeoffs, alternatives | Yes — written from the intake conversation |
| `<LOBESPACE>_<WORK>_LOG.md` | Append-only session log; one entry per implementation session | No — header only; the first session appends the first entry |
| `<LOBESPACE>_<WORK>_BURNDOWN.md` | Finishing checklist: everything between working code and a merged PR | No — template checklist |
| `<LOBESPACE>_<WORK>_CLAUDE.md` | Carries the work-item **header** (objective · branch join-key · blocked-by) and the runbook for automated tests; defers to the platform runbook, then adds work-specific steps | Header yes (from the chat); test steps left as scaffold |
| `<LOBESPACE>_<WORK>_TESTING.md` | Manual test plan: steps to verify the work item by hand; folds into the owning project repo's `CLAUDE.md` at closeout | No — template scaffold |

The work item's **header** rides the top of the `<LOBESPACE>_<WORK>_CLAUDE.md` runbook — the blockquote right after its H1 — not the PLAN. The PLAN is a frozen input to code generation, often archived as soon as its code ships (code drift never flows back into the plan), whereas the runbook persists for the item's whole open life. The header's first line is the one-sentence objective; after a blank `>` line, the metadata line carries **Branch** (the work branch, which doubles as the item's join key into the project repo — name the intended branch even before it exists) and **Blocked-by** (the `<WORK>` slug of a work item this one waits on, or `—`). **There is no Status field** — status is derived live from the project repo's branch/PR state at listing time, never stored or hand-maintained. When the item concludes, its working docs move to `archive/` and it drops out of the open set.

These are **working files**, so per `CLAUDE.md` they are *not* versioned (no `> V<N>` header), are *not* added to the read index, and are not read in future sessions unless explicitly asked.

---

## 1. The intake conversation

Before scaffolding anything, have the conversation. Setup turns a settled discussion into documents; it does not invent the design. Pin down, at minimum:

- **Owning lobe** — which lobe the work belongs to: the nearest common ancestor of the lobes the work will concern. That lobe's `working/` holds the docs and its lobespace becomes their `<LOBESPACE>`. Settle this first, since it decides both. Derive the owner top-down: match the work's terms against the lobe registry's **Routes on** column to name the lobes the work will concern, then walk up to their nearest common ancestor. A work item that concerns only one lobe is owned by that lobe; one that spans two siblings is owned by their parent.
- **Work-item name** → derive the `<WORK>` slug (§2).
- **One-line definition** — what the work item is, in a sentence.
- **Problem** — what's broken or missing, and who feels it. This anchors FINDINGS.
- **Preferred approach + tradeoffs** — the chosen direction and *why*, plus the alternatives weighed and rejected. This is the heart of FINDINGS; capture the reasoning, not just the verdict.
- **Scope boundary** — what the work item explicitly does *not* touch. Goes into PLAN's "what this does NOT include"; it is the cheapest way to prevent scope creep.
- **Testing approach** — what's covered by automated tests and what can only be checked by hand. Seeds PLAN's testing section, the BURNDOWN checklist, and the runbook/testing docs.

If the chosen approach makes an existing canonical claim false (a reversal, not just an addition), note it now — record it in FINDINGS and flag it for closeout. A reversal is the one thing a wording-based grep won't catch at merge time, so the merge relies on it being called out explicitly here.

---

## 2. Derive the slug and audit what exists

**Slug.** SCREAMING_SNAKE_CASE. Not a mechanical transform of the work-item name — short and specific, and distinct in the **prefix** sense: the procedures find an item's docs by the glob `<LOBESPACE>_<WORK>_*`, so `<LOBESPACE>_<WORK>_` must not begin any canonical document's name or another open item's compound, and no other item's compound may begin this one's — a slug `PLUM` beside an item slugged `PLUM_JAM` would sweep that item's docs into its own closeout. Also pick the slug so that no other lobe's lobespace is a longer prefix of `<LOBESPACE>_<WORK>` than `<LOBESPACE>` itself: ownership goes to the longest match, so a parent's slug that continues into a child's lobespace hands the item's files to that child.

**Audit (this is what makes setup safe on partial/existing work items).** Before creating anything, list the owning lobe's `working/` and `archive/` for the slug. From the owning lobe's directory — the repo root for hub-owned items:

```bash
find working archive -maxdepth 1 -name '<LOBESPACE>_<WORK>_*.md' 2>/dev/null
```

A lobe missing one of the two directories is normal and doesn't hide the other's matches. Empty output means a brand-new item **only if the command ran in the owning lobe's directory** — confirm the location before trusting an empty audit, because everything below builds on it.

Classify each doc:
- **Missing** — create from the template (§3).
- **Exists in `working/`** — leave it. Do not overwrite. If the intake chat adds genuinely new material, append it; never rewrite existing working content from a setup run.
- **Exists in `archive/`** — already implemented and retired (as a `<LOBESPACE>_<WORK>_PLAN.md` often is once its plan has shipped). Do **not** recreate it in `working/`; note that it is done and move on.

A brand-new work item has nothing on disk, so the full set is created. A partial one (commonly PLAN+FINDINGS) gets only its missing docs created.

---

## 3. Generate the docs

Create each missing doc in the owning lobe's `working/`, substituting `<LOBESPACE>` (the owning lobe's lobespace), `<WORK>` (SCREAMING_SNAKE), `<Work-Item Name>` (Title Case), and `<work-branch>` — a single branch name, or a glob when the item will land across several branches/PRs. Create that `working/` if the lobe does not have one yet. Fill PLAN and FINDINGS with real content from the intake chat; leave the others as scaffolds for the implementer.

Do not add a `> V<N>` version header to any of these — working files are unversioned. Do not copy them into `archive/` (that happens only at closeout). Do not touch the read index or any canonical doc.

### PLAN template

````markdown
# <Work-Item Name>: Implementation Plan

## Objective

<one paragraph from the intake chat: what the work item does and the high-level approach. Close with the "no new X" constraints if any — e.g. "No new infrastructure, no database changes.">

## Context

See `<LOBESPACE>_<WORK>_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `<LOBESPACE>_SCOPE.md` — problem space this fits into
- `<LOBESPACE>_FINDINGS.md` — relevant prior decisions
- `<LOBESPACE>_APPROACH.md` — design constraints

## What changes

<the concrete edits, file by file. Fill in during/just before implementation; leave a stub here at setup if the details aren't settled yet.>

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
|  |  |  |

## Testing approach

<automated: unit vs. integration, new test classes anticipated, what regression suite must stay green. Manual steps live in `<TOKEN>_<WORK>_TESTING.md`.>

## Implementation sequence

1.

## Scope boundary — what this does NOT include

- <the explicit non-goals settled in the chat>

## Open issues

1. <unresolved tradeoffs or decisions deferred to implementation>
````

### FINDINGS template

````markdown
# <Work-Item Name>: Decision Record

## Problem

<the problem from the chat: what's broken/missing, who feels it, why the status quo is inadequate.>

## Preferred approach: <short name>

<the chosen direction and how it works.>

| Aspect | Detail |
|---|---|
|  |  |

- **<property>** — <why this approach wins on it>

## Alternatives considered

- **<alternative>** — <what it was and why it was rejected.>

## What this doesn't solve

- <limitations that remain even within the chosen approach — every ground-truth FINDINGS doc carries this section.>

## Reversals

<If this work item makes an existing canonical claim false, name the exact claim and file here. `VV_WORK_CLOSEOUT.md` will reconcile it in place at merge. Delete this section if nothing is reversed.>
````

### LOG template

````markdown
# <Work-Item Name>: Session Log

Running log of implementation sessions. Each session appends after a `---` separator.

The first entry, and every one after it, follows the entry format and content rules in `VV_SESSION_CLOSEOUT.md` — that spec is the authority, not the prior entry, since a fresh LOG file has none to copy.
````

### BURNDOWN template

````markdown
# <Work-Item Name>: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `<work-branch>` off the default branch
  * commit changes on branch
  * create draft PR
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `<LOBESPACE>_<WORK>_CLAUDE.md`
  * manual checks — capture steps in `<LOBESPACE>_<WORK>_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* <this item's own: ports, backports, follow-on items discovered during implementation>
````

### CLAUDE (runbook) template

````markdown
# <Work-Item Name>: Claude Runbook

> <one-line objective — what this work item delivers, in a sentence.>
>
> **Branch:** `<work-branch>` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step N — <work-specific test> ← NEW in this branch

```bash
# fill in once the work item has tests
```

**Expected:** <runtime, pass/fail expectations, which tests are active>
````

### TESTING template

````markdown
# <Work-Item Name>: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout these fold into the owning project repo's `CLAUDE.md`.

## Setup

<prerequisites: config flags, roles/users, sample data needed before the steps below>

## Test cases

1. **<case name>** — the steps to exercise it by hand.
   - **Expected:** <observable result>
````

---

## 4. Handoff

After creating the docs:

1. Report the owning lobe, the slug used, which docs were **created**, and which already **existed** (and where — `working/` or `archive/`).
2. Remind that these are working files: they stay out of the read index, and the canonical mini-brain is untouched until the work concludes.
3. Point at `VV_WORK_CLOSEOUT.md` as the closeout bookend — it consumes exactly these docs.