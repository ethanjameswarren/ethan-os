"""Thin CLI for the lore-book renderer."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from .html_renderer import render_html
from .pdf import render_pdf, render_pdf_pages_to_png
from .publication import assemble_book, load_project
from .validator import validate, validate_output


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
    parser.add_argument("--skip-pngs", action="store_true", help="Skip rendering PDF pages to PNGs.")
    parser.add_argument("--png-dir", type=Path, help="Directory for PNG page renders.")
    args = parser.parse_args(argv)

    life_dir = args.life_dir
    if not life_dir:
        # cli.py lives at ethan-os/scripts/hobby/lore_book/cli.py; ethan-life is a sibling of ethan-os.
        life_dir = Path(__file__).resolve().parents[4] / "ethan-life"
    life_dir = Path(life_dir)

    edition, outline, lore_entries, media_entries, section_map = load_project(
        life_dir,
        project=args.project,
        edition_year=args.edition,
        edition_id=args.edition_id,
    )

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

        if not args.skip_pngs:
            png_dir = args.png_dir or output_path.parent / "pages"
            render_pdf_pages_to_png(pdf_path, png_dir)

        validation = validate_output(output_path, pdf_path)
        print("\nPostflight validation:")
        print(f"  HTML pages: {validation['html_page_count']}")
        print(f"  PDF pages:  {validation['pdf_page_count']}")
        print(f"  Page count match: {validation['page_count_match']}")
        print(f"  PDF size 6x9 OK: {validation['size_ok']}")
        if validation["overflows"]:
            print(f"  Overflows: {len(validation['overflows'])}")
            for o in validation["overflows"]:
                print(f"    - {o}")
        if validation["image_overruns"]:
            print(f"  Image overruns: {len(validation['image_overruns'])}")
            for o in validation["image_overruns"]:
                print(f"    - {o}")
        if validation["missing_backgrounds"]:
            print(f"  Missing backgrounds: {len(validation['missing_backgrounds'])}")
            for o in validation["missing_backgrounds"]:
                print(f"    - {o}")
        if validation["invalid_templates"]:
            print(f"  Invalid templates: {len(validation['invalid_templates'])}")
            for o in validation["invalid_templates"]:
                print(f"    - {o}")

        validation_path = output_path.with_suffix(".validation.json")
        validation_path.write_text(json.dumps(validation, indent=2, default=str), encoding="utf-8")
        print(f"Validation report: {validation_path}")

        if not validation["page_count_match"] or not validation["size_ok"] or validation["overflows"]:
            print("Validation failed — see report for details.", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
