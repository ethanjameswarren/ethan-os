# Skill: compress-to-platform-limit

## Purpose

Fit generated career content within platform-specific character, section, and formatting constraints without distorting meaning or dropping evidence-backed claims.

## Inputs

- Draft platform content
- Target platform (`linkedin`, `indeed`, `resume`, `cover-letter`, or other)
- Specific section being compressed (headline, about, summary, experience bullet, cover letter paragraph, etc.)
- Evidence-backed claims that must be preserved if possible

## Platform limits

Maintain these defaults unless the user provides current platform guidance:

### LinkedIn

- Headline: ~220 characters
- About: ~2,600 characters (older limit); prefer concise, scannable paragraphs
- Experience description per role: ~2,000 characters
- Featured section title: ~100 characters
- Project title: ~100 characters
- Project description: ~2,000 characters

### Indeed

- Professional summary / profile: ~500 characters
- Resume summary: 2–4 sentences
- Experience bullets: concise, scannable; no fixed hard limit, but prefer short
- Skills list: platform-managed; supply strongest evidence-backed terms

### Resume

- 1–2 pages for most seniorities
- Bullets: 1–2 lines
- Summary: 3–5 lines

### Cover letter

- 250–400 words unless application specifies otherwise
- 3–5 paragraphs

## Compression techniques

Apply in order:

1. Remove filler words and generic phrases.
2. Replace repeated concepts with a more precise term.
3. Combine closely related bullets if the combined claim remains evidence-backed.
4. Remove lower-priority supporting details while preserving the core claim and metric.
5. Use abbreviations or shorthand only when widely understood in the field.
6. Shorten long phrases without changing technical meaning.
7. If still over limit, drop the least important claim and note the trade-off.

## Rules

- Never drop the only evidence-backed claim in a section.
- Never invent a metric or scope detail to make a compression work.
- Preserve the original meaning; do not turn a strong claim into a vague one.
- Mark any trade-off where a significant detail was removed.
- Do not compress by removing all specificity.

## Output

Return the compressed text, the final character/word count, and a list of any sacrifices or trade-offs made.

## Confirmation policy

- Auto-execute: compressing draft content within documented platform limits.
- Ask for confirmation: when compression requires removing a claim the user may want to keep, or when multiple reasonable compression options exist.
