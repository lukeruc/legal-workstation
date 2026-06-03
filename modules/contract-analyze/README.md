# Contract Analyze Skill

A [Claude Code](https://claude.ai/code) skill for comprehensive AI-powered analysis of legal contracts using a project-manager pattern with specialized sub-agents.

## Overview

This skill enables deep structural and textual analysis of complex legal contracts in Markdown format. It mimics a legal project manager workflow: two mandatory sub-agents perform first-pass reading and cross-reference mapping, then the project manager (Claude) plans a tailored analysis strategy, deploys specialized sub-agents, integrates their outputs, and delivers a structured set of navigable documents.

The output includes party profiles, a term definitions dictionary, clause analysis grouped by theme, cross-reference mapping, conflict detection, quality validation, and more — all cross-linked with wiki links for easy navigation.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                   Phase 1: Overview                  │
│  ┌──────────────┐  ┌──────────────────┐             │
│  │ Overview     │  │ Reference Mapper │             │
│  │ Agent        │  │ Agent            │             │
│  └──────┬───────┘  └────────┬─────────┘             │
│         │ briefing.md       │ cross-ref-report.md    │
│         └────────┬──────────┘                       │
│                  ▼                                  │
│          Phase 2: Dynamic Sub-Agents                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │
│  │ Party    │ │ Clause   │ │ Terminology      │    │
│  │ Analyzer │ │ Grouper  │ │ Extractor        │    │
│  └──────────┘ └──────────┘ └──────────────────┘    │
│                  ▼                                  │
│          Phase 3: Integration                       │
│                  ▼                                  │
│          Phase 4: Structured Output                 │
└─────────────────────────────────────────────────────┘
```

1. **Phase 1 — Overview Agent** reads the full contract and produces a structured briefing (contract identity, party profiles, clause landscape, notable features). **Reference Mapper** traces cross-references, dependency chains, potential conflicts, and hidden dependencies.

2. **Phase 2 — Dynamic Sub-Agents** are created based on what the briefing reveals. Complex contracts may spawn 8–10 specialized agents; simple ones may need only 2–3. The project manager determines the right set per contract.

3. **Phase 3 — Integration** merges all sub-agent outputs into coherent documents with consistent terminology, verified cross-references, and quality checks.

4. **Phase 4 — Delivery** produces a structured `output/` directory with an index, party profiles, clause analysis, definitions, and a validation report — all in Markdown with wiki links for navigation.

## Usage

Invoke the skill with a Markdown contract file:

```
/contract-analyze path/to/contract.md
```

**Only Markdown (.md) files are accepted.** For PDFs, DOCX, or scanned documents, convert to Markdown first — preserving heading hierarchy and clause numbering.

## Output Structure

```
sessions/{task-id}/
├── original/                   # Original contract file
└── output/
    ├── index.md                # Master overview and navigation
    ├── structure.md            # Contract structure analysis
    ├── parties/                # Party profiles
    │   ├── _index.md
    │   └── {party-name}.md
    ├── definitions.md          # Term definitions dictionary
    ├── clauses/                # Clause analysis by theme
    │   ├── _index.md
    │   └── {topic}.md
    ├── validation-report.md    # Quality validation findings
    ├── open-questions.md       # Open issues and ambiguities
    └── _internal/              # PM working documents
        ├── briefing.md
        └── cross-ref-report.md
```

## Quality Standards

- **Coverage**: >95% of significant clauses addressed in output
- **Accuracy**: Clause references, amounts, dates, and party names verified
- **Consistency**: Terminology used consistently across all documents
- **Traceability**: Every analytical conclusion references the source clause

## Disclaimer

This skill provides structural and textual analysis of contracts. It does **not** provide legal advice. For legal interpretation, risk assessment, or negotiation strategy, consult a qualified lawyer.

## License

MIT © 2026
