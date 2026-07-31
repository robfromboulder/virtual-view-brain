# virtual-view-brain 🧠

```
Read ../mini-brain-toolkit/MBT_CREATE_BRAIN and **create a plan** to seed this repo as a mini-brain - don't move any files yet, let's think this through completely first!

The "virtual view brain" should cover all three of my virtual view projects: ../virtual-view-manifesto, ../viewmapper, ../viewzoo

All of these projects run on Trino platform only -- we mention that these can run on Starburst Enterprise or Starburst Galaxy but do not provide runbooks or docs or testing for Enterprise/Galaxy

Plan to use this repo for the new mini-brain, and plan to make light changes to the project repos as we merge content assets into the mini-brain

Because virtual-view-brain covers multiple projects, we'll need multiple prefixes:
* 'VV_' for standard top-level content in this brain (ie 'VV_LOG')
* 'VVM_' for content specific to virtual-view-manifesto
* 'VMR_' for viewmapper
* 'VZOO_' for viewzoo

For `virtual-view-manifesto`:
* what makes this unique - it's just a book and doesn't have runnable code (but I would like to create agentic instructions)
* do not restate all of the manifesto content in the top-level content of the mini-brain (treat the manifesto repo as ground truth just like any regular mini-brain)
* preserve CHANGES or port CHANGES content into VVM_LOG?
* plan to move TODOS into work items
* maintain local CLAUDE but move out content that doesn't belong there

For 'viewmapper':
* what makes viewmapper unique - it's the most complicated module with submodules
* 'agent' and 'mcp server' are the major modules of this project, they can be changed/tested independently and used together
* because agent/mcp use different stacks & different runbooks, recommend tracking these as VMR_AGENT_ and VMR_MCP_ assets (so we have separate logs & work items)
* READMEs should not be changed but are good information for the mini-brain
* maintain local CLAUDE files but move out content that doesn't belong there
* ARCHITECTURE and TESTING files should be merged into the mini-brain
* viewmapper has GitHub issues to import as work items

For 'viewzoo':
* what makes viewzoo unique - it's the most normal/typical of the group of 3
* viewmapper has GitHub issues to import as work items
* CLAUDE.md has both runbook and architecture information

Because of the complexity of this task, focus on creating "starter content" that seeds this brain without defining all of its higher-order functions yet. We don't need session closeout, work item setup/closeout, dream cycle, or "using mini-brain" instructions in the separate project repos yet. Focus on the organization/mapping of existing content first and then we'll come back to higher-order functions in future sessions. Do think along the way whether the proposed structure will present any problems for closeout or work item instructions, but let's not write those down until the top-level structure has been prototyped and I can review it. Do not translate all github issues into work items yet, but look at github issues to confirm the shape of the plan to import them.

As part of creating this plan, answer the following questions:
1. what would the file structure of the new mini-brain look like? (don't bother to enumerate all of the file names work items imported from GitHub, just make sure those issues fit the file/naming convention proposed) 
2. is this a reasonable or problematic application of the mini-brain pattern?
3. are any pieces of existing knowledge/instructions from existing project repos that don't fit this plan? (assuming that virtual-view-manifesto chapter content is not duplicated)
4. are there any risks or open questions you identified to address before moving forward?
5. assuming that we follow this "starter content" plan, what would be the follow-up steps that would finish out the mini-brain?

Create a plan document (VV_BOOTSTRAP_PLAN) that captures all of this information so I can review and check with other models. 
```
