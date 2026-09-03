"""Thin CLI for the lore-book renderer."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .html_renderer import render_html
from .pdf import render_pdf
from .publication import assemble_book, load_project
from .validator import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a print-ready annual lore-book HTML preview and PDF.")
    parser.add_argument("--life-dir", type=Path, help="Path to ethan-life repository root.")
    parser.add_argument("--project", default="warhammer-40k-necron-dynasty", help="Hobby project slug.")
    parser.add_argument("--edition", type=int, default=datetime.now().year, help="Edition year.")
    parser.add_argument("--edition-id", help="Optional explicit edition object ID.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    parser.add_argument("--draft", action="store_true", help="Render a draft; do not finalize the edition object.")
    parser.add_argument("--skip-pdf", action="store_true", help="Generate HTML only.")
    parser.add_argument("--skip-validation", action="store_true", help="Skip preflight validation.")
    args = parser.parse_args(argv)

    life_dir = args.life_dir
    if not life_dir:
        life_dir = Path(__file__).resolve().parents[3] / "ethan-life"
    life_dir = Path(life_dir)

    edition, outline, lore_entries, media_entries, section_map = load_project(
        life_dir,
        project=args.project,
        edition_year=args.edition,
        edition_id=args.edition_id,
    )

    project_dir = life_dir / "hobby" / args.project if False else life_dir / "domains" / "hobby" / args.project
    project_dir = life_dir / "domains" / "hobby" / args.project

    output_path = args.output
    if not output_path:
        output_dir = life_dir / "reports" / "hobby" / args.project / "lore-book" / str(args.edition)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "lore-book.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    book = assemble_book(
        edition,
        outline,
        lore_entries,
        media_entries,
        section_map,
        project_dir,
        output_path.parent / "assets",
    )

    if not args.skip_validation:
        errors = validate(book)
        if errors:
            print("Preflight errors:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            return 1

    html_doc, warnings = render_html(book)
    for w in warnings:
        print(f"Warning: {w}", file=sys.stderr)

    output_path.write_text(html_doc, encoding="utf-8")
    print(f"Lore book rendered: {output_path}")

    if not args.skip_pdf:
        pdf_path = output_path.with_suffix(".pdf")
        render_pdf(output_path, pdf_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
