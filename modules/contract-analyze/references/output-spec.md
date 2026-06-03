# Output Format Specifications

## Directory Structure

The output directory is created at `sessions/{task-id}/output/`. The exact structure is determined
by the project manager based on the contract, but follows these conventions:

```
sessions/{task-id}/output/
├── index.md                    # Master overview and navigation (REQUIRED)
├── structure.md                # Contract structure analysis
├── parties/                    # Party profiles (only if 2+ parties)
│   ├── _index.md               # Summary table + links to per-party files
│   └── {party-name}.md
├── definitions.md              # Term definitions dictionary
├── clauses/                    # Clause analysis by theme (only if 2+ topic files)
│   ├── _index.md               # Overview of categories + links
│   └── {topic}.md
├── validation-report.md        # Quality validation findings
├── open-questions.md           # Open issues
└── _internal/                  # PM working documents (not deliverables)
    ├── briefing.md             # Overview Agent report
    └── cross-ref-report.md     # Reference Mapper report
```

### When to use a directory vs. a single file

- **Single file**: When a category produces one content file, give it a descriptive name at the output
  root. Example: `definitions.md`, not `definitions/_index.md`.
- **Directory with `_index.md`**: Only when the category produces multiple files and needs a
  navigation/summary page. Example: `clauses/` with an `_index.md` linking to each topic file.

The `_index.md` inside a directory is a table-of-contents page — not the content itself. Do not hide a
content file behind the name `_index.md`.

### The `_internal/` directory

`_internal/` contains the PM's working documents from the two pre-defined agents. These are not part
of the final deliverable — they are inputs the PM uses to plan and coordinate. Users browsing the
output can ignore this directory; index.md links only to the deliverable documents.

## index.md Template

The index.md must follow this structure. Sections marked [REQUIRED] must be present; others may be
adapted or omitted based on the contract.

```markdown
# [Contract Name]

## Contract Basic Information [REQUIRED]

| Item | Content |
|------|---------|
| Contract Name | [full name] |
| Contract Type | [purchase/service/construction/NDA/...] |
| Contract Number | [if available] |
| Signing Date | [YYYY-MM-DD] |
| Effective Date | [YYYY-MM-DD] |
| Term | [fixed term/ongoing/project-based] |
| Governing Law | [jurisdiction] |
| Dispute Resolution | [arbitration/litigation, venue] |

## Parties [REQUIRED]

| Role | Name | Details |
|------|------|---------|
| [Party A role] | [name] | [[Details|parties/{filename}]] |
| [Party B role] | [name] | [[Details|parties/{filename}]] |

## Core Commercial Terms [REQUIRED if applicable]

| Item | Content | Details |
|------|---------|---------|
| Contract Value | [amount and currency] | [[Details|clauses/{filename}]] |
| Payment Terms | [summary] | [[Details|clauses/{filename}]] |
| Performance Security | [if any] | [[Details|clauses/{filename}]] |
| Key Deliverables | [summary] | [[Details|clauses/{filename}]] |
| Key Dates | [milestones] | [[Details|clauses/{filename}]] |

## Document Structure [REQUIRED]

### Contract Analysis Documents

- [[Contract Structure|structure]] — Section hierarchy and organization
- [[Party Information|parties/_index]] — Detailed party profiles
- [[Term Definitions|definitions]] — Contract terminology dictionary
- [[Clause Analysis|clauses/_index]] — Thematic clause analysis
- [[Validation Report|validation-report]] — Consistency and completeness checks
- [[Open Questions|open-questions]] — Items needing clarification

### Original Contract

- [filename] — Original Markdown contract used for analysis

## Quick Navigation

### Key Clauses

- [[Clause Description|clauses/{filename}]]
- ...

### Risk Points

- [Risk description] — [[Details|clauses/{filename}]]
- ...

## Analysis Summary

[Executive summary covering: contract type and purpose, key commercial arrangement, notable risk
allocation, unusual provisions, and overall assessment. 2-4 paragraphs.]

## Revision Record

| Date | Version | Description | Analyst |
|------|---------|-------------|---------|
| [YYYY-MM-DD] | v1.0 | Initial analysis | [Agent identifier] |
```

## Document Standards

### Wiki Links

Use the format `[[display text|relative/path/from/output]]`. Examples:
- `[[Payment Terms|clauses/commercial-terms]]`
- `[[Party A Details|parties/party-a]]`
- `[[Definitions|definitions]]`

The display text can be:
- A clause number and title: `[[Art. 5.1 - Price|clauses/commercial-terms]]`
- A descriptive label: `[[Liability Cap Analysis|clauses/risk-allocation]]`
- The document's natural title: `[[Contract Structure|structure]]`

### Backlinks

Every document must end with a Backlinks section:

```markdown
## Backlinks

- [[index]] — Main index
- [[Other Document|path/to/doc]] — Why it links here
```

### Source References

When referencing the original contract, always include the clause/section identifier:

```markdown
The Seller must deliver within 30 days of receiving the purchase order (Art. 4.2).
```

For direct quotations, use blockquotes:

```markdown
> The Buyer shall pay the Contract Price within 60 days after receipt of a valid invoice. (Art. 5.1)
```

### Interpretations vs. Facts

Clearly distinguish factual summary from analytical interpretation:

```markdown
**Summary:** The contract specifies a 60-day payment term (Art. 5.1).

**Analysis:** This is longer than market standard (typically 30 days), which may indicate
the Seller has accepted extended payment terms, possibly in exchange for other concessions.
```

### Source Labels

Every factual claim must carry a source label following the convention in
`playbook/process/information.md`:

| Label | Meaning |
|-------|---------|
| `[contract — Clause X]` | Sourced from the contract under analysis |
| `[user provided]` | Instructions or information from user |
| `[model knowledge — verify]` | General legal knowledge, not verified against a database |
| `[briefing — Clause X]` | Sourced from the Overview Agent's briefing (secondary source) |

The label describes provenance, not confidence. Do not upgrade a label because something
"feels right."

### _index.md Files

`_index.md` files are navigation pages only — not content. They exist only when a directory has
multiple files and needs a summary page. A directory with a single file should not exist; use a
flat file at the output root instead.

When used, an `_index.md` should:
1. Summarize what the directory covers
2. List and briefly describe each file in the directory
3. Link to each file using Wiki Links

## Quality Markers

In validation documents, use these markers for clarity:

| Marker | Meaning |
|--------|---------|
| ✅ | Verified correct |
| ⚠️ | Potential issue / needs review |
| ❌ | Error or inconsistency found |
| ❓ | Unclear / ambiguous |
| 📝 | Note / observation |
