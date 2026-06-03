---
name: contract-analyze
description: >-
  Invoked via /contract-analyze. Analyzes a Markdown contract file using a project-manager pattern
  with pre-defined and dynamic sub-agents. Produces structured output with index, party profiles,
  clause analysis, term definitions, cross-reference mapping, and validation.
---

# Contract Analysis Skill

## Overview

This skill enables comprehensive analysis of complex legal contracts. The approach mimics a legal project
manager: delegate the first-pass reading to a specialist, receive a structured briefing, plan an analysis
strategy, delegate to specialized sub-agents, and finally integrate everything into a structured set of
documents.

There are exactly **two pre-defined sub-agents** that run for every contract:

1. **Overview Agent** — reads the full contract and produces a structured briefing
2. **Reference Mapper** — traces cross-references, dependencies, and conflicts between clauses

These two provide the PM with both an aerial map and a connection analysis before any planning
decisions are made. Every other analysis dimension, sub-agent type, and output organization
decision is dynamic, based on what these two reports reveal.

## Input Validation

**Only Markdown (.md) contract files are accepted.**

When a user provides a contract for analysis, first check the file format. If the file is NOT a `.md` file
(PDF, DOCX, scanned image, etc.), respond with:

> This skill only processes Markdown (.md) contract files. Please convert your contract to Markdown format
> and resubmit. When converting, preserve the original document's heading hierarchy and clause numbering.
>
> Suggested conversion approaches:
> - PDF/Word documents: use a conversion tool to extract text, then format as Markdown
> - Scanned documents: perform OCR first, then format as Markdown
> - For best results, ensure section numbers, clause references, and heading levels are preserved

Do not attempt to convert or process non-Markdown files. If the user insists, explain that format
conversion errors can cause analysis mistakes, and the skill is designed specifically for text-based
contract analysis.

If the file IS a `.md` file, proceed to Phase 1.

## The Project Manager Pattern

You are the project manager for this contract analysis. Think of yourself as a senior legal project
manager who:

- Delegates first-pass reading to the Overview Agent and connection analysis to the Reference Mapper
- Reads their reports, not the raw contract, to form strategy
- Plans work strategically based on what the briefing and cross-reference report reveal
- Delegates detailed analysis to specialized sub-agents with clear, bounded tasks
- Reviews and integrates their work into a coherent whole
- Ensures quality, consistency, and completeness

As project manager, you do NOT do the detailed analysis yourself — and you do not read the full contract
yourself. Your primary jobs are planning, coordination, integration, and quality assurance. Delegate the
reading to the Overview Agent, delegate connection analysis to the Reference Mapper, and delegate
substantive analysis to specialized sub-agents.

## Infrastructure Context

The following are already loaded in context by the host environment (CLAUDE.md):

- **`.claude/profiles/`** — User's company, role, jurisdiction, language, output preferences.
  Use these to: identify the user's company when it appears as a party, contextualize
  governing law analysis against the user's known jurisdictions, and format outputs
  according to user preferences.
- **`playbook/process/approach.md`** — Task classification rules
- **`playbook/process/information.md`** — Source labeling, jurisdiction awareness, file coverage
- **`playbook/process/role.md`** — Role boundaries: provide analysis, not decisions

If profiles are empty (cold start not run), proceed without and note this limitation.

## Phase 0: Workspace Setup

Before any analysis, create the session directory:

1. Generate a task ID: `{YYYY-MM-DD}-{contract-slug}` where slug is derived from the contract filename
2. `mkdir -p sessions/{task-id}/original/`
3. `mkdir -p sessions/{task-id}/output/_internal/`
4. Copy the contract file to `sessions/{task-id}/original/`

All analysis outputs will be written to `sessions/{task-id}/output/`.

## Phase 1: Overview and Plan

### 1.1 Spawn the Overview Agent

**This step is mandatory for every contract.** The Overview Agent is the first of two pre-defined
sub-agents. It reads the full contract and produces a structured briefing document.

Read `agents/overview-agent.md` for the Overview Agent's full instructions. Spawn it as a sub-agent using
the Agent tool with:

- The file path to `agents/overview-agent.md` as its instruction source
- The contract file path substituted for `[CONTRACT_PATH]`
- Instruction to save its output to `sessions/{task-id}/output/_internal/briefing.md`

The Overview Agent produces `sessions/{task-id}/output/_internal/briefing.md` containing:
- Contract identity (type, purpose, governing law, template)
- Scale and complexity assessment
- Party identification with roles and characteristics
- Core commercial arrangement summary
- Complete clause landscape (every major section summarized)
- Notable features (one-sided terms, missing provisions, ambiguities, risks)
- Suggested analysis dimensions

### 1.2 Spawn the Reference Mapper

**This step is mandatory for every contract.** Once the Overview Agent completes and
`sessions/{task-id}/output/_internal/briefing.md` exists, spawn the Reference Mapper as the second pre-defined sub-agent.

Read `agents/reference-mapper.md` for the Reference Mapper's full instructions. Spawn it with:

- The file path to `agents/reference-mapper.md` as its instruction source
- The contract file path substituted for `[CONTRACT_PATH]`
- Instruction to save its output to `sessions/{task-id}/output/_internal/cross-ref-report.md`

The Reference Mapper produces `sessions/{task-id}/output/_internal/cross-ref-report.md` containing:
- Explicit cross-reference matrix (every clause that references another, and how)
- Dependency chains (A → B → C cascading dependencies)
- Potential conflicts and tensions (clauses that appear to contradict each other, with severity ratings)
- Hidden dependencies (clauses governing overlapping subject matter without explicit references)
- Orphan references (references to clauses or exhibits that don't exist)
- Definition drift (terms that shift meaning across sections)
- Structural tensions (important provisions buried in unexpected places)

### 1.3 Read Both Reports and Draft the Plan

Read `sessions/{task-id}/output/_internal/briefing.md` and `sessions/{task-id}/output/_internal/cross-ref-report.md` thoroughly.

Before relying on the briefing for planning, spot-check it: pick 2-3 clauses at random from
the briefing's Clause Landscape, read those clauses in the original contract, and verify the
briefing's summary is accurate. Also check the Reference Mapper's Briefing Validation section
for any errors it flagged. If the briefing has significant errors, spawn a corrected Overview
Agent run before proceeding.

Do NOT read the full contract yourself beyond this spot-check. These two reports are your
primary input for planning. (You will do deeper contract checking later during quality verification.)

Pay particular attention to the Reference Mapper's conflict and tension findings. If it flagged
high-severity conflicts between specific clauses, your plan should assign a sub-agent to
investigate those areas in depth.

Based on the briefing, draft an analysis plan. This is an internal working document, not part of the
final output. The plan should cover:

1. **Analysis dimensions**: Which aspects of this contract need dedicated analysis? The Overview Agent
   provided suggestions — use them as a starting point, but apply your own judgment. Some dimensions may
   need splitting; others may be combined. Consider:
   - Party details (obligations, rights, risks by party)
   - Definitions and key terms
   - Commercial terms (pricing, payment, delivery, acceptance)
   - Risk allocation (warranties, indemnities, limitations of liability)
   - Legal and governance provisions
   - Structure and organization
   - Term and termination
   - Cross-references and dependencies
   - Any special dimensions unique to this contract

2. **Sub-agent assignments**: For each analysis dimension, decide:
   - Needs a dedicated sub-agent (complex, requires focused attention)
   - Can be combined with another dimension (simple, closely related topics)
   - Can be covered using briefing content directly — too simple to need a sub-agent

3. **Execution order**: Identify dependencies. For example:
   - Terminology extraction should complete before clause analysis (so analysts use consistent terms)
   - Party analysis and clause analysis can run in parallel
   - If the cross-ref report flagged specific conflict areas, assign sub-agents to investigate those
   - Quality checking must come last, after all other outputs exist

4. **Output structure**: Sketch the planned directory structure. Start from the common pattern in Phase 4
   and adapt it to this contract's specifics.

### 1.4 Validate the Plan

Before creating sub-agents, sanity-check your plan:

- Does every significant clause category from the briefing's Clause Landscape have an owner?
- Have the Reference Mapper's high-severity conflict areas been assigned for investigation?
- Are sub-agent scopes clear and non-overlapping?
- Is the output structure appropriate for this contract's complexity?
- Are there any gaps — topics mentioned in either report but not assigned?

## Phase 2: Deploy Sub-Agents

Create and launch the sub-agents defined in your plan. The Overview Agent and Reference Mapper have
already provided the high-level briefing and connection analysis — these sub-agents do the deep,
detailed analysis.

### 2.1 Sub-Agent Design Principles

Each sub-agent you create should have:

- **A clear, specific goal** — "Analyze Article 5 (Price and Payment)" not "Look at the money stuff"
- **Well-defined boundaries** — The sub-agent knows exactly which clauses or topics it owns, based on
  the clause ranges identified in the briefing
- **Self-contained input** — The sub-agent receives the contract file path and specific section ranges
  to read
- **Expected output format** — Tell the sub-agent what its output file should contain and how to
  structure it
- **Traceability requirement** — Instruct the sub-agent to reference original clause numbers and quote
  key language

### 2.2 Creating Sub-Agents

Use the Agent tool to create sub-agents. For each sub-agent:

1. **Write a detailed prompt** that includes:
   - The specific task and its scope (clause ranges from the briefing)
   - The contract file path
   - The expected output file path and format
   - Quality requirements (accuracy, traceability, completeness)
   - Any relevant context from the briefing, cross-ref report, or other completed sub-agent outputs

2. **Launch independent sub-agents in parallel** when they have no dependencies. For example, party
   analysis, terminology extraction, and clause grouping can all run simultaneously.

3. **Sequence dependent sub-agents**. If the clause analysis sub-agents need the terminology dictionary,
   run the terminology sub-agent first, then launch the clause sub-agents.

### 2.3 Common Sub-Agent Types

The following are common sub-agent patterns for contract analysis. The Overview Agent and Reference
Mapper (Phase 1) have already run — these types are for deeper, focused analysis. Adapt and combine
them based on the specific contract and your plan.

See `references/sub-agent-guide.md` for detailed task prompt templates for each type.

| Sub-Agent Type | Purpose | Typically Produces |
|----------------|---------|-------------------|
| Structure Analyzer | Detailed heading hierarchy, clause numbering scheme, exhibit/schedule relationships, structural anomalies | `structure.md` |
| Party Analyzer | Detailed party obligations, rights, representations, warranties, special conditions per party | `parties/{party-name}.md` |
| Terminology Extractor | Build a complete definitions dictionary; flag undefined terms, unused definitions, inconsistencies | `definitions.md` |
| Clause Grouper | Group related clauses by theme and provide detailed analysis of each group | `clauses/{group-name}.md` |
| Commercial Terms Extractor | Extract pricing, payment, delivery, acceptance terms in detail | `clauses/commercial-terms.md` |
| Risk Analyzer | Analyze risk allocation: indemnities, liability caps, warranties, insurance, penalties | `clauses/risk-allocation.md` |
| Conflict Investigator | Investigate specific conflicts or tensions flagged by the Reference Mapper | `clauses/conflict-analysis.md` |
| Quality Checker | Verify consistency, completeness, numerical accuracy across all outputs | `validation-report.md` |

**Important**: These are starting points, not a checklist. Create the sub-agents that make sense for
THIS contract. If a contract is a simple NDA, you might need only 2-3 sub-agents. For a complex
construction contract, you might need 8-10. If none of the above patterns fit, create custom types.

### 2.4 Monitoring Sub-Agent Progress

Sub-agents run asynchronously. As each completes:
- Review its output against the briefing for completeness and quality
- Note any issues that might affect other sub-agents
- If a sub-agent's output is incomplete or low-quality, create a follow-up sub-agent to fix specific
  issues, or fix minor issues yourself

## Phase 3: Integrate Results

Once all sub-agents have completed, integrate their outputs into a coherent document set.

### 3.1 Create the Index

Create `sessions/{task-id}/output/index.md` following the template in `references/output-spec.md`. The index is the entry
point for the entire analysis. It must include:

- Contract basic information table
- Party summary with links
- Core commercial terms summary with links
- Document structure (links to all output files)
- Quick navigation to key clauses
- Risk points summary
- Analysis summary (your executive overview)
- Revision record

### 3.2 Verify Cross-References

- Ensure all `[[Wiki Links]]` point to existing files
- Add Backlinks sections to each document listing which documents link to it
- Verify that clause references (numbers, titles) are accurate

### 3.3 Quality Verification

Perform a quality review using the briefing as your reference:

1. **Coverage check**: Compare the briefing's Clause Landscape against the sub-agent outputs. Is every
   significant clause group addressed somewhere? Aim for >95% coverage.

2. **Accuracy spot-check**: Delegate to a Quality Checker sub-agent (see `references/sub-agent-guide.md`
   for its task template). It will verify clause references, amounts, dates, and obligations against the
   original contract.

3. **Consistency check**: Are the same terms used consistently across all documents? Do any two
   documents contradict each other?

4. **Gap filling**: If you find gaps, create targeted sub-agents to fill them, or address minor gaps
   yourself.

5. **Open questions**: Document anything ambiguous, contradictory, or unclear in `open-questions.md`.

### 3.4 Structure Optimization

Review the output directory structure:

- Merge overly granular documents (a single short clause doesn't need its own file)
- Split overly long documents (a 50-clause group should be broken down)
- Ensure filenames are lowercase, hyphen-separated, and descriptive
- Only create a subdirectory when a category genuinely contains multiple files. A single-file category
  should be a file at the output root, not a directory with a single `_index.md`

## Phase 4: Deliver Output

### 4.1 Final Output Structure

The output directory is at `sessions/{task-id}/output/`. Structure it like:

```
sessions/{task-id}/
├── original/                   # Original contract file
│   └── contract.md
└── output/
    ├── index.md                # Master overview and navigation (REQUIRED)
    ├── structure.md            # Contract structure analysis
    ├── parties/                # Party profiles (only if 2+ parties)
    │   ├── _index.md           # Summary table + links to per-party files
    │   └── {party-name}.md
    ├── definitions.md          # Term definitions dictionary
    ├── clauses/                # Clause analysis by theme (only if 2+ topic files)
    │   ├── _index.md           # Overview of categories + links
    │   └── {topic}.md
    ├── validation-report.md    # Quality validation findings
    ├── open-questions.md       # Open issues and ambiguities
    └── _internal/              # PM working documents (not deliverables)
        ├── briefing.md         # Overview Agent report
        └── cross-ref-report.md # Reference Mapper report
```

**`_index.md` files serve exactly one purpose**: navigation pages for multi-file directories. They
summarize what the directory covers and link to each file. When a category produces only a single
file, give it a descriptive name at the output root — do not wrap it in a directory with a lone
`_index.md`.

The exact structure depends on the contract. The above is a common pattern, not a requirement.

### 4.2 Document Standards

All output documents must follow these standards:

- **Markdown format** with consistent heading hierarchy
- **Lowercase filenames** with hyphens (e.g., `commercial-terms.md`)
- **Backlinks section** at the end of each document listing inbound links
- **Source references** for every factual claim (clause number, section, or page)
- **Wiki Links** using `[[display text|relative/path]]` format for cross-references
- **Clear labeling** of interpretations vs. facts (use "Analysis:" or "Interpretation:" prefixes for
  analytical commentary)

### 4.3 Present Results to User

When the analysis is complete, present a summary to the user:

1. State what the contract is and its key characteristics
2. Highlight the most important findings (commercial terms, risks, unusual provisions)
3. Point to the output directory and index.md
4. Note any open questions or areas needing human review
5. Remind the user that this is structural analysis, not legal advice

## Quality Standards

Follow the baseline rules in `playbook/process/information.md` for source labeling, jurisdiction
awareness, and file coverage. Sub-agents have their own quality requirements specific to their tasks.

If quality cannot be met (e.g., the contract is extremely complex or contains ambiguous language),
document the limitations in `open-questions.md`.

## Important Disclaimers

- This skill provides structural and textual analysis of contracts. It does NOT provide legal advice.
- For legal interpretation, risk assessment, or negotiation strategy, the user should consult a
  qualified lawyer.
- The analysis is only as good as the input. If the Markdown conversion introduced errors or omissions,
  the analysis will reflect those.
- Multi-contract analysis (comparing contracts, analyzing contract networks) requires additional human
  oversight.
