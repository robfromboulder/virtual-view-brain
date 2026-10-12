# Virtual View: Visual Design

> V3, 2026-10-12.

The virtual view projects share one visual design system for README images and published pages. This file records where it lives, why it looks the way it does, and how to use it. The design system states the rules; this file holds the reasons and the addresses.

---

## 1. Pages

| Page | URL |
| --- | --- |
| Virtual View Visual Design (the design system) | https://claude.ai/artifact/J4FgVd16GZaxG8UQ7EPsdh |

The design system is the authority, and the READMEs that use it are its worked examples. It is owned by robfromboulder and shared publicly.

---

## 2. Decisions

**Lettering.** The drafter's text has to read in quantity on a busy blue grid and still look drawn by hand. Patrick Hand SC is the face that does both. Real handwriting (Caveat) is reserved for the checker, so the personality sits where the jokes are.

**Casing.** Everything the drafter letters is in capitals, as in drafting and comic lettering. It reads as lettering rather than typing, and it avoids Patrick Hand SC's small caps: fed lowercase, they sit well below the font's straight apostrophe, which floats above the word, and the small-cap f is drawn in lowercase form. The drafter's text uses the curly apostrophe. The checker writes in ordinary case, so the two voices differ in form as well as color. Identifiers keep their real case because they are code a reader may type.

**The checker is rationed.** Yellow notes are the most fun part of a sheet and the quickest to turn into clutter. One per frame or sheet, each a real claim the project makes, keeps the humor from becoming glib.

**Pencil gray is set by contrast.** Pencil gray is `#cddbec`, 4.65:1 on the blue ground, so small text meets 4.5:1.

**Text stays text.** An all-SVG README suits a portal that only points at published pages. These READMEs carry install steps, code and prose that must stay copyable, searchable and readable by agents, and the manifesto's own scope asks that an agent can answer from its text. Sheets frame the markdown; they never replace it. GitHub's alerts stay native rather than drawn, because they carry GitHub's theme colors and meaning. Anything a reader needs from a sheet is repeated in text.

**Only the opening sheet is drawn.** Each README opens with one sheet for human readers: the hero for a tool, the comic page for the manifesto. Everything after it is portable markdown, with `##` headings, Mermaid diagrams, code and alerts. Chapter sheets in place of headings were tried on viewzoo and viewmapper and dropped. Mermaid stays because an agent reads its source as text, while an exported sheet's lettering is outlined paths that leave an agent only the alt text. The manifesto is meant to become an agentic toolkit, so its diagrams stay Mermaid too.

**The opening sheet tells a story.** It shows the project's highest-order concepts, never an index. The table of contents is text below it, not part of the drawing.

**The brain's README is an index.** Only its owner uses it, to maintain the other projects and as a reference example of a working multi-lobe mini-brain, so nothing in it needs to be copied, searched or navigated. One index sheet carries the brain and the usage prompts, link cards point to the projects, and alt text carries every word. It is the one exception to text staying text and to the opening sheet telling a story.

**The brain's lobes are captioned by role.** Anatomical names (frontal, parietal, occipital) were meant as analogies and didn't land with the first reader. Each lobe now says what it is: the hub, the manifesto, the zoo, the mapper, the MCP server.

**The toolkit strip carries the toolkit's mark.** The 🧠 is mini-brain-toolkit's identity, not decoration, so it is the one emoji in the system. It is embedded as vector art (Noto Color Emoji, Apache 2.0), so it doesn't depend on the viewer's emoji font.

**Wobble is baked at export.** On GitHub, the displacement filter broke thin lines into offset segments. Sources keep the live filter so a drawing stays editable, and the export replaces it with displaced linework.

**Lettering stays off major grid lines.** A major line running through a line of lettering reads as a strike-through. A label centered in a cake tier may cross one when moving it off would crowd the tier.

**README images share one paragraph, and tile gaps live in the images.** GitHub puts paragraph margin between paragraphs but not between lines, and spaces and margins don't scale with the images, so gaps set in markup came out uneven. A transparent margin drawn into each tile scales with it. `align="top"` removes the space a browser leaves under an image in a line of text, and whole-number frame sizes stop browsers rounding a tile smaller than its neighbors.

**Every README image sits inside a link.** GitHub wraps any image left outside a link in a link to the raw file, so clicking the hero opened a bare SVG. A sheet that points nowhere gets an inert link of its own, `#`.

---

## 3. Using It

- Before drawing anything, read the design system's `project/README.md` with the Artifact tool's `read` action, then the card for each component you use. Start new sheets from the matching component preview, or from a shipped sheet where §4 names that preview as stale, not from memory.
- Use the cast as the design system assigns it: every sheet for a project draws that project's subject.
- Commit images under each project repo's `.github/images/`, exported by this repo's `.github/images/text2path.py`, which outlines the lettering and bakes the wobble. Keep the editable `*.src.svg` sources beside them so a note can change without redrawing letters.
- When a decision changes the system, change the design system's files and record the reason in §2. Update only the design-system files the change touches; the artifact's own instructions cover how.

---

## 4. Open Questions

- Whether narrow sheet variants served through `<picture>` media queries work on GitHub for phone widths is untested.
- The GitHub social preview image (1280 × 640) has no design yet.
- Minimum text sizes are stated at 1200-wide scale, but link cards shown three across render smaller: their 12px meta line comes out near 9px.
- Other repos have no copy of the export script or its fonts, and whether they call this repo's copy or carry their own is undecided.
- The HeroSheet, IndexSheet and PhasingSheet previews predate the shipped sheets: they draw the brain's old anatomical captions and title blocks with sheet codes and drawn and checked cells. Each needs redrawing from a shipped sheet.
- No shipped sheet is a standalone PhasingSheet; the only phasing row is inside the manifesto's comic page. Whether to keep it for a future hero or fold it into ComicPage is undecided.
- Every shipped hero sets its title-block field names at 10px, below the 12px minimum the design system states for `tb-field`. Either the heroes are re-exported at 12px or the minimum exempts title-block fields.
