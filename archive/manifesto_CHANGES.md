# Change Log

## Version 0.69 (2026-01-08)
- Added architectural diagram comparing virtual views vs microservices abstraction layers
- Reframed "Why Not Just Use ORMs or Microservices?" with clearer use-case guidance
- Expanded principle 2 with advanced example showing layer replacement in action
- Added principle 2 caution callouts about ANSI/ISO SQL standardization and platform variance
- Removed "what's novel" and "what's controversial" from introduction
- Fixed broken links in principles contents

## Version 0.68 (2026-01-07)
- Revised and expanded use cases
- Tweaked use case order again 🤞
- Disabled implementation notes for now

## Version 0.67 (2026-01-02)
- Reordered use cases 3-7 for stronger narrative arc and pedagogical flow

## Version 0.66 (2026-01-02)
- Edits to principles, expand copy and improve examples
- Swapped order of principles 2 and 3
- Tweaked principle titles

## Version 0.65 (2025-12-30)
- Added TODOS.md to track suggestions and questions
- Minor tweaks to language in a few spots

## Version 0.64 (2025-12-30)
- **Reordered "what's novel" and "what's controversial" sections**
- Moved from header to end of introduction for better context and flow
- Readers now understand the pattern before evaluating novelty and controversy

## Version 0.63 (2025-12-30)
- **Editorial refinements to header and introduction sections**
- Better acknowledge the concerns of the skeptical reader
- Contrast "virtualization at query engine layer" as a new option alongside microservices & ORMs

## Version 0.62 (2025-12-21)
- **Fixed SECURITY INVOKER in Python code examples**
- Affected Use Case 2 (Testing Data Edge Cases) and Use Case 5 (Runtime Configuration)
- Ensures consistency with SECURITY INVOKER convention across all example types

## Version 0.61 (2025-12-21)
- **Fixed section file formatting for IntelliJ IDEA compatibility**
- All section files now start with empty line before `---` delimiter
- Fixes Structure view navigation and syntax highlighting for IDEA
- No impact on build.sh output; purely for editor compatibility

## Version 0.60 (2025-12-21)
- **Refactored README into modular section files** for improved maintainability
- Created 10 section files in `sections/` directory (00-header through 09-footer)
- Added `build.sh` script to generate README.md from section files
- Updated `.claudeignore` to exclude generated README.md from context loading
- Section files are now the source of truth for all edits
- Added section file formatting convention (consistent delimiters and spacing)
- Updated CLAUDE.md with build workflow documentation
- **Added SECURITY INVOKER to CREATE VIEW examples** throughout the manifesto
- Added "Using SECURITY INVOKER in Examples" section to CLAUDE.md documenting the convention
- SECURITY INVOKER omitted from Introduction (classical views), Principle 6 counter-examples, and SELECT statements
- Document remains at ~1960 lines, ~9,300 words

## Version 0.53 (2025-12-18)
- **Improved examples and diagrams** throughout the document for clarity and consistency
- Enhanced Mermaid diagrams with better formatting and visual clarity
- Refined SQL examples to better demonstrate three-level naming conventions
- No structural changes; improvements focused on presentation quality

## Version 0.52 (2025-12-16)
- **Merged Implementation Guide and Appendix** to eliminate duplication and improve flow
- Eliminated redundant Steps 3, 5, 6 (generic examples superseded by e-commerce example)
- Removed standalone "Appendix: Complete Example" section
- Updated Table of Contents to remove Appendix link
- Document reduced from 1998 to 1963 lines, ~9,000 words
- Net change: 35 lines reduced

## Version 0.51 (2025-12-16)
- **Refined all eight use case challenge/solution statements** for clarity, specificity, and value proposition
- **Added "Use Case Selection Criteria" section** to CLAUDE.md emphasizing virtual view patterns over Trino-specific features
- No structural changes; document remains at 1998 lines, ~9,200 words

## Version 0.5 (2025-12-16)
- **Major restructuring**: Eliminated "Practical Patterns" and "View Lifecycle Management" sections
- Merged Pattern 2 (Prototyping Progression) into Use Case 1 with Gantt timeline diagram
- Created Use Case 4 from Pattern 3 (Per-Feature Hierarchies / Isolating Per-Feature Storage)
- Created Use Case 5 from Pattern 4 (Runtime Configuration Switching)
- Removed Pattern 1 (Three-Layer Stack) as redundant with other content
- Moved bottom-up replacement guidance from View Lifecycle to Use Case 3
- Moved view deletion guidance to new Pitfall 5 (Attempting to Delete Base Views)
- Reordered use cases for pedagogical flow: prototyping → testing → schema evolution → feature isolation → runtime config → privacy → Iceberg → cost routing
- Renamed Use Case 6 from "Enforcing Privacy and Compliance Controls" to "Ensuring Privacy and Compliance"
- Added link tables (numbered lists with anchors) to Common Pitfalls and When NOT to Use sections for easier navigation
- Use Case 8 (Cost and Availability Routing) left as stub for future completion
- Document reduced from 2189 to 1998 lines, ~9,200 words
- Net change: 191 lines reduced

## Version 0.4 (2025-12-16)
- Reordered Common Pitfalls by decreasing impact and frequency (Type Mismatch → Forgetting Dependents → Breaking Assumptions → Permissions → Lost Definitions → Circular Dependencies)
- Consolidated Anti-Patterns 1 & 4 ("Over-Abstraction" and "Single-Layer Hierarchies") into single section
- Reduced anti-pattern count from 4 to 3
- Voice improvements: "A single view is meh" and other conversational tweaks
- Added practical guidance: test migrations in dev/staging, consider sorting in application code
- Net change: 45 lines reduced (119 deletions, 75 insertions)
- Document reduced from 2234 to 2189 lines, ~9,600 words
