# Evaluation Criteria

## Deterministic checks

- Valid YAML frontmatter.
- Schema identifier resolves in registry.
- Required fields present.
- Provenance present.
- Relationship target IDs exist.
- Duplicate IDs not created.

## AI-quality checks

- Capture fidelity: does the processed object preserve the user's meaning?
- Source/user belief separation: are source claims and Ethan-position kept distinct?
- Duplicate prevention: are substantively identical ideas linked rather than duplicated?
- Relationship quality: are relationships meaningful and justified?
- Summary usefulness: does the summary include personal interpretation and disagreement?
- Portability/readability: are files plain Markdown with minimal frontmatter?
- Excessive object creation: is the system creating objects for every sentence?

## Human review

- Did the user need to administer the system manually?
- Did the system ask for confirmation only when meaningful?
- Are summaries genuinely personal?
