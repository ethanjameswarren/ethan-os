#!/usr/bin/env python3

import argparse
import html
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml

GROUP_ORDER = ["Characters", "C'tan", "Infantry", "Destroyers", "Canoptek", "Other"]


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def newest_points(records: list[dict[str, Any]]) -> dict[tuple[str, int], dict[str, Any]]:
    newest: dict[tuple[str, int], dict[str, Any]] = {}
    priority = {"standard": 2, "first_unit": 1, "subsequent_unit": 0}
    for record in records:
        key = (record["unit_id"], record["unit_size"])
        current = newest.get(key)
        if current is None or priority.get(record.get("cost_tier", "standard"), -1) > priority.get(current.get("cost_tier", "standard"), -1) or (priority.get(record.get("cost_tier", "standard"), -1) == priority.get(current.get("cost_tier", "standard"), -1) and record.get("verified_date", "") > current.get("verified_date", "")):
            newest[key] = record
    return newest


def points_for_quantity(unit_id: str, quantity: int, points: dict[tuple[str, int], dict[str, Any]]) -> int | None:
    options = sorted((size, record["value"]) for (candidate, size), record in points.items() if candidate == unit_id and size <= quantity)
    totals: list[int | None] = [0] + [None] * quantity
    for current in range(1, quantity + 1):
        candidates = [totals[current - size] + value for size, value in options if size <= current and totals[current - size] is not None]
        totals[current] = max(candidates) if candidates else None
    return totals[quantity]


def summarize(project: Path) -> dict[str, Any]:
    collection_data = load_yaml(project / "collection" / "inventory.yaml")
    points_data = load_yaml(project / "rules" / "points" / "current.yaml")
    purchase_data = load_yaml(project / "purchases" / "plan.yaml")
    list_data = load_yaml(project / "army-lists" / "lists.yaml")
    paint_data = load_yaml(project / "painting" / "scheme-references.yaml")
    collection = collection_data.get("collection", [])
    purchases = [item for item in purchase_data.get("purchases", []) if item.get("status") in {"planned", "ordered"} and item.get("quantity", 0) > 0]
    points = newest_points(points_data.get("points", []))

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    energy = defaultdict(lambda: {"painted": 0, "total": 0})
    owned_points = 0
    owned_points_complete = True
    for item in collection:
        value = points_for_quantity(item["unit_id"], item["quantity_owned"], points)
        rendered = dict(item, current_points=value)
        groups[item.get("collection_group", "Other")].append(rendered)
        if value is None and item["quantity_owned"]:
            owned_points_complete = False
        else:
            owned_points += value or 0
        energy[item["energy_scheme"]]["painted"] += item["quantity_painted"]
        energy[item["energy_scheme"]]["total"] += item["quantity_owned"]

    planned_points = 0
    planned_points_complete = True
    planned = []
    for item in purchases:
        value = points_for_quantity(item["unit_id"], item["quantity"], points)
        planned.append(dict(item, current_points=value))
        if value is None:
            planned_points_complete = False
        else:
            planned_points += value

    owned = {item["unit_id"]: item["quantity_owned"] for item in collection}
    concepts = []
    for army in list_data.get("lists", []):
        selections = army.get("units", [])
        missing = []
        total = 0
        points_complete = True
        for selection in selections:
            quantity = selection["quantity"]
            available = owned.get(selection["unit_id"], 0)
            if quantity > available:
                missing.append({"unit_id": selection["unit_id"], "required": quantity, "owned": available, "missing": quantity - available})
            value = points_for_quantity(selection["unit_id"], selection.get("unit_size", quantity), points)
            if value is None:
                points_complete = False
            else:
                total += value
        if not selections:
            status = "DRAFT"
        elif missing:
            status = "MISSING MODELS"
        elif points_complete and total == army.get("target_points"):
            status = "READY"
        else:
            status = "DRAFT"
        concepts.append(dict(army, status=status, missing=missing, current_points=total if points_complete else None))

    model_count = sum(item["quantity_owned"] for item in collection)
    assembled = sum(item["quantity_assembled"] for item in collection)
    painted = sum(item["quantity_painted"] for item in collection)
    planned_models = sum(item["quantity"] for item in purchases)
    points_source = points_data.get("source", {})
    datasheets = [load_yaml(path) for path in sorted((project / "rules" / "datasheets").glob("*.yaml"))]
    rules_dates = [sheet.get("source", {}).get("last_verified_at") for sheet in datasheets if sheet.get("source", {}).get("last_verified_at")]
    rules_versions = {sheet.get("source", {}).get("faction_pack_version") for sheet in datasheets if sheet.get("source", {}).get("faction_pack_version")}
    rules_status = "red" if not datasheets else "yellow" if any(sheet.get("verification_status") != "verified" for sheet in datasheets) else "green"
    points_status = "green" if points_data.get("verification_status") == "verified" else "yellow"
    return {
        "model_count": model_count,
        "unit_types": len(collection),
        "assembled": assembled,
        "painted": painted,
        "remaining": model_count - painted,
        "paint_percent": round(painted * 100 / model_count) if model_count else 0,
        "planned_models": planned_models,
        "owned_points": owned_points if owned_points_complete else None,
        "planned_points": planned_points if planned_points_complete else None,
        "projected_points": owned_points + planned_points if owned_points_complete and planned_points_complete else None,
        "projected_models": model_count + planned_models,
        "last_points_verification": points_source.get("last_verified_at"),
        "rules_version": ", ".join(sorted(rules_versions)) if rules_versions else None,
        "rules_last_verified": max(rules_dates) if rules_dates else None,
        "rules_status": rules_status,
        "points_version": points_source.get("version"),
        "points_status": points_status,
        "groups": groups,
        "roles": [group for group in GROUP_ORDER if groups.get(group)],
        "energy": energy,
        "planned": planned,
        "concepts": concepts,
        "paint_scheme": paint_data.get("dynasty_paint_scheme", {}),
        "generated_date": date.today().isoformat(),
    }


def esc(value: Any) -> str:
    return html.escape(str(value))


def points_text(value: int | None) -> str:
    return f"{value:,} pts" if value is not None else "Needs verification"


def render(summary: dict[str, Any]) -> str:
    cards = [
        ("Owned models", summary["model_count"]),
        ("Current points", points_text(summary["owned_points"])),
        ("Assembled", summary["assembled"]),
        ("Painted", summary["painted"]),
        ("Still to paint", summary["remaining"]),
        ("Planned models", summary["planned_models"]),
        ("Points verified", summary["last_points_verification"] or "Not yet"),
    ]
    group_html = []
    for group in GROUP_ORDER:
        items = summary["groups"].get(group, [])
        if not items:
            continue
        rows = []
        for item in items:
            assembly = f'{item["quantity_assembled"]}/{item["quantity_owned"]} assembled'
            painting = f'{item["quantity_painted"]}/{item["quantity_owned"]} painted'
            rows.append(f'<tr><td><strong>{esc(item["unit"])}</strong></td><td>{item["quantity_owned"]}</td><td>{points_text(item["current_points"])}</td><td>{assembly}</td><td>{painting}</td><td><span class="energy {esc(item["energy_scheme"])}">{esc(item["energy_scheme"].title())}</span></td></tr>')
        group_html.append(f'<section><h3>{esc(group)}</h3><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Quantity</th><th>Points</th><th>Assembly</th><th>Paint</th><th>Energy</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')

    energy_rows = "".join(f'<li><span class="energy {name}">{name.title()}</span><strong>{values["painted"]} / {values["total"]}</strong> painted</li>' for name, values in summary["energy"].items())
    planned_rows = []
    for item in summary["planned"]:
        planned_rows.append(f'<tr><td><strong>{esc(item["unit"])}</strong> ×{item["quantity"]}</td><td>{points_text(item["current_points"])}</td><td>{esc(item.get("priority") or "Not ranked")}</td><td>{esc(item["status"].title())}</td><td>{esc(item.get("strategic_reason") or "Not recorded")}</td></tr>')
    concept_cards = []
    for concept in summary["concepts"]:
        missing = ""
        if concept["missing"]:
            details = ", ".join(f'{entry["unit_id"]} ×{entry["missing"]}' for entry in concept["missing"])
            missing = f'<p class="missing">Required: {esc(details)}</p>'
        concept_cards.append(f'<div class="concept"><span class="status {concept["status"].lower().replace(" ", "-")}">{concept["status"]}</span><strong>{esc(concept["name"])}</strong><span>{points_text(concept["current_points"])}</span>{missing}</div>')

    card_html = "".join(f'<div class="stat"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in cards)
    role_html = "".join(f'<span class="role">{esc(role)}</span>' for role in summary["roles"])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Necron Collection Overview</title><style>
:root{{--bg:#0b0f12;--panel:#131a1f;--line:#26323a;--text:#edf4f3;--muted:#9aaba9;--cyan:#35d9e6;--red:#ff5757;--purple:#b57aff;--green:#78d6a3}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 system-ui,sans-serif}}main{{max-width:1180px;margin:auto;padding:28px}}h1{{margin:0;font-size:2.25rem}}h2{{margin:34px 0 12px}}h3{{margin:22px 0 8px;color:#cdd9d7}}.hero{{padding:24px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(135deg,#152127,#101519)}}.headline{{font-size:1.1rem;color:var(--muted);margin:5px 0 18px}}.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(135px,1fr));gap:9px}}.stat{{background:#0d1317;border:1px solid var(--line);border-radius:10px;padding:11px}}.stat span{{display:block;color:var(--muted);font-size:.78rem}}.stat strong{{font-size:1.05rem}}.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:10px}}table{{width:100%;border-collapse:collapse;background:var(--panel)}}th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}}th{{color:var(--muted);font-size:.75rem;text-transform:uppercase}}tr:last-child td{{border-bottom:0}}.energy,.status,.role{{display:inline-block;border-radius:999px;padding:3px 8px;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em}}.fresh{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-top:12px}}.fresh .panel{{display:flex;gap:10px;align-items:center}}.dot{{width:11px;height:11px;border-radius:50%;flex:none}}.dot.green{{background:#42d392}}.dot.yellow{{background:#f4c152}}.dot.red{{background:#ff5757}}.cyan{{color:var(--cyan);background:#12333a}}.red{{color:var(--red);background:#3a1719}}.purple{{color:var(--purple);background:#291b3d}}.paint-grid,.projection{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}.panel,.concept{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}.bar{{height:14px;background:#253038;border-radius:99px;overflow:hidden}}.bar i{{display:block;height:100%;background:linear-gradient(90deg,var(--cyan),var(--purple));width:{summary["paint_percent"]}%}}ul{{padding-left:0;list-style:none}}li{{display:flex;gap:9px;align-items:center;margin:7px 0}}li strong{{margin-left:auto}}.role{{background:#1b292f;color:#c9dad7;margin:3px}}.concept{{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;margin:8px 0}}.ready{{background:#153525;color:var(--green)}}.draft{{background:#2b3034;color:#c4ced0}}.missing-models{{background:#3a2317;color:#ffb36b}}.missing{{grid-column:2/-1;color:#ffb36b;margin:0}}.projection strong{{display:block;font-size:1.35rem}}.meta{{color:var(--muted);font-size:.82rem}}@media(max-width:700px){{main{{padding:14px}}.concept{{grid-template-columns:1fr}}.missing{{grid-column:auto}}}}
</style></head><body><main>
<header class="hero"><h1>Necron Collection</h1><p class="headline"><strong>{summary["model_count"]} Models</strong> · <strong>{summary["unit_types"]} Unit Types</strong> · <strong>{points_text(summary["owned_points"])}</strong></p><div class="stats">{card_html}</div><div class="fresh"><div class="panel"><i class="dot {summary["rules_status"]}"></i><div><strong>Rules</strong><div class="meta">11th Edition · Necrons v{esc(summary["rules_version"] or "unverified")} · Verified {esc(summary["rules_last_verified"] or "never")}</div></div></div><div class="panel"><i class="dot {summary["points_status"]}"></i><div><strong>Points</strong><div class="meta">MFM v{esc(summary["points_version"] or "unverified")} · Verified {esc(summary["last_points_verification"] or "never")}</div></div></div></div></header>
<h2>Current Collection</h2>{''.join(group_html)}
<h2>Army Composition</h2><div class="panel"><p class="meta">Roles and model families represented in the physical collection</p>{role_html}</div>
<h2>Painting Summary</h2><div class="paint-grid"><div class="panel"><strong>Dynasty Scheme</strong><p>Black armor · Silver skeleton</p><p class="meta">Energy communicates role/status; it is not the predominant armor color.</p></div><div class="panel"><strong>Painted: {summary["painted"]} / {summary["model_count"]}</strong><p>{summary["paint_percent"]}% complete</p><div class="bar"><i></i></div><ul>{energy_rows}</ul></div></div>
<h2>Planned Expansion</h2><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Current points</th><th>Priority</th><th>Status</th><th>Strategic purpose</th></tr></thead><tbody>{''.join(planned_rows)}</tbody></table></div>
<h2>Collection After Planned Purchases</h2><div class="projection"><div class="panel"><span class="meta">Current Collection</span><strong>{summary["model_count"]} models</strong><span>{points_text(summary["owned_points"])}</span></div><div class="panel"><span class="meta">Planned Additions</span><strong>{summary["planned_models"]} models</strong><span>{points_text(summary["planned_points"])}</span></div><div class="panel"><span class="meta">Projected Collection</span><strong>{summary["projected_models"]} models</strong><span>{points_text(summary["projected_points"])}</span></div></div>
<h2>Available Army Concepts</h2>{''.join(concept_cards)}
<p class="meta">Generated {summary["generated_date"]} from canonical collection, points, painting, purchase, and army-list data. This page is a derived view and must not be edited as a source of truth.</p>
</main></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Necron Collection Overview")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output or project.parents[2] / "reports" / "hobby" / project.name / "reports" / "collection-overview.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(summarize(project)), encoding="utf-8")
    print(f"Collection overview generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
