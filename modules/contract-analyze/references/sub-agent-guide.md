# Sub-Agent Guide

This reference provides detailed task descriptions for common sub-agent types used in contract analysis.
The project manager should adapt these based on the specific contract.

## Structure Analyzer

**Purpose**: Map the contract's organizational structure.

**Task prompt template**:

```
Analyze the structure of the contract at [file path]. Produce sessions/{task-id}/output/structure.md containing:

1. A table showing the top-level heading hierarchy (section numbers, titles, page numbers if available)
2. For each major section, a 1-2 sentence summary of what it covers
3. Identification of any schedules, exhibits, or appendices and their relationship to the main body
4. A note on the clause numbering scheme (sequential, hierarchical, article-based, etc.)
5. Any structural anomalies (missing numbers, duplicate headings, inconsistent nesting)

Reference the original contract's exact heading text and clause numbers throughout.
```

## Party Analyzer

**Purpose**: Extract and profile each party to the contract.

**Task prompt template**:

```
Analyze all parties mentioned in the contract at [file path]. For each distinct legal entity, create a
file at sessions/{task-id}/output/parties/{party-slug}.md containing:

1. Full legal name, any abbreviations used, and registered address if stated
2. Role in the contract (buyer/seller, client/provider, etc.)
3. Primary obligations — what must this party do or deliver?
4. Primary rights — what is this party entitled to receive or enforce?
5. Key representations and warranties made by this party
6. Any special conditions, qualifications, or limitations specific to this party
7. All clause references where this party's obligations/rights appear

Also create sessions/{task-id}/output/parties/_index.md with a summary table of all parties and links.

Quote key contractual language and cite clause numbers for every claim.
```

## Terminology Extractor

**Purpose**: Build a dictionary of defined terms.

**Task prompt template**:

```
Extract all defined terms from the contract at [file path]. Produce sessions/{task-id}/output/definitions.md with:

1. A table listing each defined term, its definition, and the clause where it's defined
2. For terms used across multiple clauses, note where they are most heavily used
3. Flag any terms that are:
   - Defined but never used
   - Used but never defined
   - Defined differently in different places (inconsistency)
4. Identify any capitalized terms that appear to be defined terms but lack a formal definition

Use the exact wording of definitions from the contract. Cite clause numbers.
```

## Clause Grouper

**Purpose**: Group related clauses by theme and summarize each group.

**Task prompt template**:

```
Analyze the contract at [file path] and group its clauses into thematic categories.
For each category, create sessions/{task-id}/output/clauses/{category-slug}.md containing:

1. A summary of what this category of clauses addresses
2. A table listing each clause in the category (number, title, 1-line summary)
3. Detailed analysis of the most important clauses in the category
4. Notable provisions, unusual terms, or potential concerns
5. Cross-references to related clauses in other categories

Determine the categories based on what makes sense for THIS contract, not a preset list.
Common categories might include: commercial terms, risk allocation, performance standards,
legal provisions, term and termination, etc.

Also create sessions/{task-id}/output/clauses/_index.md with a summary of all categories and links.

Cite clause numbers and quote key language throughout.
```

## Commercial Terms Extractor

**Purpose**: Detailed extraction of pricing, payment, delivery, and acceptance terms.

**Task prompt template**:

```
Extract all commercial and financial terms from [file path]. Produce sessions/{task-id}/output/clauses/commercial-terms.md:

1. Pricing structure (unit prices, total value, currency, taxes, adjustments)
2. Payment schedule and conditions (milestones, triggers, documentation required)
3. Delivery terms (Incoterms, timelines, partial delivery rules)
4. Acceptance criteria and procedures
5. Price adjustment mechanisms (indexation, variation orders, change orders)
6. Financial security requirements (bonds, guarantees, letters of credit, retention)
7. Late payment provisions (interest, suspension rights)

For every amount, date, and percentage, quote the exact contract language and cite the clause.
Flag any amounts that appear inconsistent with each other.
```

## Risk Analyzer

**Purpose**: Analyze risk allocation provisions.

**Task prompt template**:

```
Analyze the risk allocation provisions in [file path]. Produce sessions/{task-id}/output/clauses/risk-allocation.md:

1. Warranty and guarantee provisions — scope, duration, remedies
2. Indemnification provisions — triggers, scope, procedures, limitations
3. Limitation of liability — caps, exclusions, carve-outs
4. Insurance requirements
5. Force majeure provisions — scope, consequences, notification
6. Liquidated damages and penalty clauses
7. Consequential damages exclusions
8. Any one-sided or unusual risk allocations

For each provision, note whether it is mutual or one-sided, and cite the clause.
Flag provisions that appear unusually favorable to one party.
```

## Conflict Investigator

**Purpose**: Investigate specific conflicts or tensions flagged by the Phase 1 Reference Mapper.

**Task prompt template**:

```
The Reference Mapper flagged the following conflict(s) in sessions/{task-id}/output/_internal/cross-ref-report.md:

[List the specific conflicts with clause references]

Investigate these conflicts in depth. Read the relevant clauses in [contract path] and produce
sessions/{task-id}/output/clauses/conflict-analysis.md:

1. For each conflict:
   - Quote the exact language from both clauses
   - Explain the nature of the tension in plain language
   - Analyze which clause would likely prevail under the governing law (if determinable from the contract text)
   - Assess the practical risk: what scenario would trigger this conflict?
2. Note any other clauses that might affect the resolution of the conflict
3. If the conflict appears to be a drafting error, suggest how it might be resolved
4. Rate each conflict: [critical / significant / minor] based on the potential impact

Cite clause numbers and quote key language throughout.
```

## Reference Mapper

**Note**: The Reference Mapper is now a pre-defined mandatory agent that runs in Phase 1. See
`agents/reference-mapper.md` for its full instructions. The template below is retained for
reference and for cases where the PM needs a deeper follow-up investigation.

**Purpose**: Map cross-references, dependencies, and potential conflicts between clauses.

**Task prompt template**:

```
Map all cross-references in [file path]. Produce sessions/{task-id}/output/_internal/cross-ref-report.md containing:

1. An explicit cross-reference matrix: for each clause that references another, list the source and
   target clause numbers and the nature of the reference (incorporation, exception, condition, etc.)
2. Identify dependency chains (A → B → C) where clauses cascade
3. Flag potential conflicts: clauses that appear to contradict each other (with quotes from both)
4. Identify "orphan" references: clauses referenced but not present in the document
5. Note any circular references or self-referential clauses

Use a table format for the matrix. For each conflict, quote both clauses and explain the tension.
```

## Quality Checker

**Purpose**: Verify consistency, completeness, and accuracy.

**Task prompt template**:

```
Perform quality validation on the contract analysis outputs in the sessions/{task-id}/output/ directory.
Produce sessions/{task-id}/output/validation-report.md:

1. Cross-check 10 randomly selected clause numbers in the analysis documents against the original
   contract — are they correct?
2. Verify all defined terms are used consistently across all output documents
3. Check that all monetary amounts, dates, and percentages in the analysis match the original contract
4. Scan the original contract for any significant clause that was NOT addressed in the analysis
5. Check all Wiki Links in the output documents — do they point to existing files?
6. Verify the index.md contains all required sections

Use ✅ / ⚠️ / ❌ markers for each check. For every issue found, provide:
- The specific location (file, section)
- The nature of the issue
- A suggested fix
```
