# Ethan OS Resume Template

Canonical LaTeX resume template for the `build-tailored-resume` workflow.

## Files

- `resume.tex` — the main document, populated by the resume builder workflow.
- `ethan-resume.sty` — centralized style package containing all typography, spacing, color, and layout decisions.

## Design decisions

The visual design is a direct translation of `ethan-life/global/design-philosophy.md` into resume-specific decisions:

- **Restrained and precise**: no decorative sidebars, progress bars, skill ratings, icons, or heavy boxes.
- **Premium but honest**: clean hierarchy and efficient whitespace rather than ornate styling.
- **Modern and minimal**: single-column structure, sentence-case section titles, whitespace-driven hierarchy, efficient margins.
- **Typography**: TeX Gyre Heros (via the `tex-gyre` package) for a clean, modern sans-serif; `microtype` for refined text.
- **Header**: left-aligned name and contact line with restrained separators, no centered academic treatment.
- **Color**: near-black body text, gray metadata, and a single restrained deep-steel-blue accent reserved for rare structural emphasis.
- **Spacing scale**: consistent section and list spacing defined in `ethan-resume.sty`, avoiding brittle negative spacing hacks.

## ATS compromises

The design prioritizes, in order:

1. Accurate content
2. ATS parsing
3. Readability
4. Information hierarchy
5. Efficient use of space
6. Personal design expression

Specific compromises made in service of ATS compatibility:

- Single-column layout (avoids parser column-confusion).
- Standard document flow; no text boxes, graphics, tables for primary content, or decorative floats.
- Real text for all important information; no graphical skill indicators.
- Standard, widely available fonts (TeX Gyre Heros is a standard Helvetica-style sans-serif).
- No horizontal rules or decorative graphics; all content is plain text in standard document flow.

## How the workflow injects content

The `build-tailored-resume` workflow writes content into the commands at the top of `resume.tex`. Presentation is fully controlled by `ethan-resume.sty`.

```latex
\name{Ethan Warren}
\contacts{City, ST ~|~ email@example.com ~|~ linkedin.com/in/...}
\summary{...}
\skills{...}
\experience{...}
\projects{...}
\education{...}
```

Each section command is a plain macro. The workflow generates the LaTeX body for each macro from the canonical `career.resume` object.

### Experience / project / education entries

Use the `\resumeentry` command:

```latex
\resumeentry{Role Title}{Employer}{Date Range}{Location}
\begin{itemize}
  \item Accomplishment bullet with evidence-backed impact.
\end{itemize}
```

The fourth argument (location) is optional; pass an empty `{}` to omit it.

## Customization

Adjust presentation globally in `ethan-resume.sty`:

- `margin`, `top`, `bottom` in the `geometry` package call.
- Font size and family.
- Section title format and color.
- List spacing and indentation.

Do not embed career facts or job-specific formatting into the style file. Content belongs in `resume.tex` or in the `career.resume` object.
