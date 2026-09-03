#!/usr/bin/env python3
"""
Generate lightweight digital hobby reports from Ethan Life data.

Report types:
- collection: owned/planned units, build/paint/magnetization state, gaps
- battles: battle chronology, outcomes, opponents, candidate lore
- rules: dynamic tabletop reference placeholder

These reports are operational/digital artifacts and intentionally NOT part of the
annual print lore book.
"""

from __future__ import annotations

import argparse
import html
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


DEFAULT_PROJECT = "warhammer-40k-necron-dynasty"
DOMAIN = "hobby"


def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def _load_objects(directory: Path) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    if not directory.exists():
        return objects
    for path in directory.rglob("*.md"):
        try:
            data = _parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data:
            objects.append(data)
    return objects


def _h(value: Any) -> str:
    return html.escape(str(value) if value is not None else "")


def _css() -> str:
    return """
    :root { --bg: #fff; --fg: #111; --muted: #666; --border: #ddd; --cyan: #0d9488; --red: #b91c1c; --purple: #7e22ce; }
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--fg); margin: 0; padding: 2rem; line-height: 1.5; }
    h1, h2 { font-weight: 600; }
    h1 { font-size: 1.6rem; border-bottom: 2px solid var(--border); padding-bottom: .5rem; }
    h2 { font-size: 1.2rem; margin-top: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { text-align: left; padding: .5rem; border-bottom: 1px solid var(--border); }
    th { color: var(--muted); font-weight: 600; font-size: .85rem; }
    .meta { color: var(--muted); font-size: .9rem; margin-bottom: 1rem; }
    .status-owned { color: #15803d; }
    .status-wishlist { color: #b45309; }
    .status-victory { color: #15803d; }
    .status-defeat { color: var(--red); }
    .status-draw { color: var(--purple); }
    .card { border: 1px solid var(--border); border-radius: .5rem; padding: 1rem; margin-top: 1rem; }
    .card h3 { margin: 0 0 .5rem 0; font-size: 1rem; }
    .tag { display: inline-block; background: #f3f4f6; padding: .1rem .4rem; border-radius: .25rem; font-size: .8rem; color: #374151; }
"""


def _render_collection_report(collection: list[dict[str, Any]]) -> str:
    rows = []
    owned = planned = 0
    for item in sorted(collection, key=lambda x: x.get("title", "")):
        ps = item.get("purchase_status", "unknown")
        if ps == "owned":
            owned += item.get("quantity", 0)
        else:
            planned += item.get("quantity", 0)
        rows.append(
            f"<tr><td>{_h(item.get('title'))}</td>"
            f"<td class=\"status-{_h(ps)}\">{_h(ps)}</td>"
            f"<td>{_h(item.get('quantity'))}</td>"
            f"<td>{_h(item.get('assembly_status', 'unknown'))}</td>"
            f"<td>{_h(item.get('painting_status', 'unknown'))}</td>"
            f"<td>{_h(item.get('magnetization_status', 'unknown'))}</td></tr>"
        )
    summary = f"""
    <p class=\"meta\">Total owned models: {owned} &nbsp;|&nbsp; Total planned/wishlist models: {planned}</p>
    <table>
      <thead><tr><th>Unit / Kit</th><th>Status</th><th>Qty</th><th>Assembly</th><th>Painting</th><th>Magnetization</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """
    gaps = [it for it in collection if it.get("purchase_status") != "owned"]
    gap_html = ""
    if gaps:
        gap_html += "<h2>Acquisition Gaps</h2><ul>"
        for g in gaps:
            gap_html += f"<li>{_h(g.get('title'))} — {_h(g.get('purchase_status'))}</li>"
        gap_html += "</ul>"
    return summary + gap_html


def _render_battle_chronicle(battles: list[dict[str, Any]]) -> str:
    if not battles:
        return "<p>No battle reports on record.</p>"
    rows = []
    for b in sorted(battles, key=lambda x: x.get("played_date", "")):
        result = b.get("result", "unknown")
        rows.append(
            f"<tr><td>{_h(b.get('played_date'))}</td>"
            f"<td>{_h(b.get('opponent_faction'))}</td>"
            f"<td class=\"status-{_h(result)}\">{_h(result)}</td>"
            f"<td>{_h(b.get('points'))}</td>"
            f"<td>{_h(b.get('scenario'))}</td>"
            f"<td>{_h(b.get('outcome_summary', ''))[:120]}</td></tr>"
        )
    return f"""
    <table>
      <thead><tr><th>Date</th><th>Opponent</th><th>Result</th><th>Points</th><th>Scenario</th><th>Summary</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """


def _render_rules_reference() -> str:
    return """
    <p>This report is intentionally a lightweight, dynamic reference for current tabletop rules, points, stats, and abilities. It is not part of the annual print lore book.</p>
    <div class="card"><h3>Current Rules Snapshot</h3><p class="meta">No specific edition or points data has been stored yet. Populate this report with the current game system edition, codex version, and any dynasty-specific rules references.</p></div>
    <div class="card"><h3>Points Summary</h3><p class="meta">Not tracked yet.</p></div>
    <div class="card"><h3>Army List Reference</h3><p class="meta">Not tracked yet.</p></div>
    """


def main():
    parser = argparse.ArgumentParser(description="Generate a digital hobby report.")
    parser.add_argument("report_type", choices=["collection", "battles", "rules"], help="Type of report.")
    parser.add_argument("--life-dir", type=Path, help="Path to ethan-life repository root.")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="Hobby project slug.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    args = parser.parse_args()

    life_dir = args.life_dir
    if not life_dir:
        life_dir = Path(__file__).resolve().parents[3] / "ethan-life"
    life_dir = Path(life_dir)

    project_dir = life_dir / "domains" / DOMAIN / args.project

    title = f"Hobby Digital Report — {args.report_type.title()}"
    if args.report_type == "collection":
        items = _load_objects(project_dir / "collection")
        body = _render_collection_report(items)
    elif args.report_type == "battles":
        battles = _load_objects(project_dir / "battles")
        body = _render_battle_chronicle(battles)
    else:
        body = _render_rules_reference()

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{_h(title)}</title><style>{_css()}</style></head>
<body>
<h1>{_h(title)}</h1>
<p class="meta">Project: {_h(args.project)} &nbsp;|&nbsp; Generated: {datetime.now().strftime('%Y-%m-%d')}</p>
{body}
</body></html>
"""

    if args.output:
        output_path = args.output
    else:
        output_dir = life_dir / "reports" / DOMAIN / args.project / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{args.report_type}-report.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(doc, encoding="utf-8")
    print(f"Digital report generated: {output_path}")


if __name__ == "__main__":
    main()
