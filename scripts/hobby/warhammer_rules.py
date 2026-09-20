#!/usr/bin/env python3

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml


def load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def required_units(project: Path) -> dict[str, str]:
    collection = load(project / "collection" / "inventory.yaml").get("collection", [])
    purchases = load(project / "purchases" / "plan.yaml").get("purchases", [])
    return {item["unit_id"]: item["unit"] for item in collection + purchases if item.get("quantity_owned", item.get("quantity", 0)) > 0 and item.get("status", "owned") in {"owned", "planned", "ordered"}}


def validate(project: Path) -> list[str]:
    errors = []
    required = required_units(project)
    sheets = {path.stem: load(path) for path in (project / "rules" / "datasheets").glob("*.yaml")}
    for unit_id in required:
        sheet = sheets.get(unit_id)
        if sheet is None:
            errors.append(f"missing datasheet: {unit_id}")
            continue
        for field in ("unit_id", "unit", "faction", "edition", "profile", "ranged_weapons", "melee_weapons", "core_abilities", "army_rules", "unit_abilities", "keywords", "faction_keywords", "change_history"):
            if field not in sheet:
                errors.append(f"{unit_id}: missing {field}")
        source = sheet.get("source", {})
        for field in ("provider", "url", "faction_pack_version", "source_last_updated", "retrieved_at", "last_verified_at"):
            if source.get(field) in (None, ""):
                errors.append(f"{unit_id}: missing source.{field}")
    points = load(project / "rules" / "points" / "current.yaml")
    point_ids = {record.get("unit_id") for record in points.get("points", [])}
    for unit_id in required:
        if unit_id not in point_ids:
            errors.append(f"missing points: {unit_id}")
    return errors


def differences(old: Any, new: Any, prefix: str = "") -> list[dict[str, Any]]:
    if isinstance(old, dict) and isinstance(new, dict):
        result = []
        for key in sorted(set(old) | set(new)):
            if key in {"retrieved_at", "last_verified_at", "change_history"}:
                continue
            result.extend(differences(old.get(key), new.get(key), f"{prefix}.{key}" if prefix else key))
        return result
    if old != new:
        return [{"field": prefix, "previous": old, "new": new}]
    return []


def compare(project: Path, candidate: Path) -> dict[str, Any]:
    changed, unchanged, missing = [], [], []
    for unit_id, unit in required_units(project).items():
        current_path = project / "rules" / "datasheets" / f"{unit_id}.yaml"
        candidate_path = candidate / "datasheets" / f"{unit_id}.yaml"
        if not candidate_path.exists():
            missing.append(unit_id)
            continue
        changes = differences(load(current_path), load(candidate_path)) if current_path.exists() else [{"field": "datasheet", "previous": None, "new": "created"}]
        (changed if changes else unchanged).append({"unit_id": unit_id, "unit": unit, "changes": changes})
    current_points = project / "rules" / "points" / "current.yaml"
    candidate_points = candidate / "points" / "current.yaml"
    point_changes = differences(load(current_points), load(candidate_points)) if candidate_points.exists() else [{"field": "points", "previous": "current", "new": "candidate missing"}]
    return {"checked": date.today().isoformat(), "changed": changed, "unchanged": unchanged, "missing": missing, "points_changes": point_changes}


def apply(project: Path, candidate: Path) -> dict[str, Any]:
    report = compare(project, candidate)
    stamp = date.today().isoformat()
    history = project / "rules" / "history" / stamp
    if history.exists():
        raise ValueError(f"history snapshot already exists: {history}")
    history.mkdir(parents=True)
    shutil.copytree(project / "rules" / "datasheets", history / "datasheets")
    shutil.copytree(project / "rules" / "points", history / "points")
    for source in (candidate / "datasheets").glob("*.yaml"):
        shutil.copy2(source, project / "rules" / "datasheets" / source.name)
    shutil.copy2(candidate / "points" / "current.yaml", project / "rules" / "points" / "current.yaml")
    report_path = project / "rules" / "updates" / f"rules-update-{stamp}.yaml"
    report_path.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and compare versioned Warhammer rules snapshots")
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("--candidate", type=Path, required=True)
    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            errors = validate(args.project)
            result = {"valid": not errors, "errors": errors}
        elif args.command == "compare":
            result = compare(args.project, args.candidate)
        else:
            result = apply(args.project, args.candidate)
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
        return 0 if result.get("valid", True) else 1
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
