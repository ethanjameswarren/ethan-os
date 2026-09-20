#!/usr/bin/env python3

import argparse
import copy
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

FILES = {
    "collection": Path("collection/inventory.yaml"),
    "points": Path("rules/points/current.yaml"),
    "lists": Path("army-lists/lists.yaml"),
    "purchases": Path("purchases/plan.yaml"),
    "storage": Path("storage/locations.yaml"),
    "paint": Path("painting/scheme-references.yaml"),
}


def load(project: Path, name: str) -> dict[str, Any]:
    path = project / FILES[name]
    if not path.exists():
        raise ValueError(f"Missing canonical {name} file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save(project: Path, name: str, data: dict[str, Any]) -> None:
    (project / FILES[name]).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def keyed(items: list[dict[str, Any]], field: str = "unit_id") -> dict[str, dict[str, Any]]:
    return {item[field]: item for item in items}


def validate(project: Path) -> list[str]:
    errors: list[str] = []
    collection = load(project, "collection")
    inventory = collection.get("collection", [])
    paint = load(project, "paint").get("dynasty_paint_scheme", {})
    paint_scheme_id = paint.get("id")
    energy_schemes = set(paint.get("energy_classes", {}))
    ids: set[str] = set()
    for item in inventory:
        unit_id = item.get("unit_id")
        if not unit_id or unit_id in ids:
            errors.append(f"collection has missing/duplicate unit_id: {unit_id}")
        ids.add(unit_id)
        owned = item.get("quantity_owned")
        assembled = item.get("quantity_assembled", 0)
        painted = item.get("quantity_painted", 0)
        if not all(isinstance(value, int) and value >= 0 for value in (owned, assembled, painted)):
            errors.append(f"{unit_id}: quantities must be non-negative integers")
        elif assembled > owned or painted > assembled:
            errors.append(f"{unit_id}: require painted <= assembled <= owned")
        if item.get("paint_scheme_ref") != paint_scheme_id:
            errors.append(f"{unit_id}: paint_scheme_ref must resolve to {paint_scheme_id}")
        if item.get("energy_scheme") not in energy_schemes:
            errors.append(f"{unit_id}: unknown or missing energy_scheme")
    points_data = load(project, "points")
    points = points_data.get("points", [])
    source = points_data.get("source", {})
    for field in ("provider", "publication", "version", "retrieved_at", "last_verified_at"):
        if source.get(field) in (None, ""):
            errors.append(f"points source: missing {field}")
    known_ids = ids | {item.get("unit_id") for item in load(project, "purchases").get("purchases", [])}
    for record in points:
        if record.get("unit_id") not in known_ids:
            errors.append(f"points references unknown unit_id: {record.get('unit_id')}")
        for field in ("value", "unit_size", "cost_tier"):
            if record.get(field) in (None, ""):
                errors.append(f"points {record.get('unit_id')}: missing {field}")
    for army in load(project, "lists").get("lists", []):
        for selection in army.get("units", []):
            if selection.get("unit_id") not in ids:
                errors.append(f"list {army.get('id')} references unknown unit_id: {selection.get('unit_id')}")
            if not isinstance(selection.get("quantity"), int) or selection["quantity"] < 1:
                errors.append(f"list {army.get('id')}: quantity must be a positive integer")
    return errors


def latest_points(project: Path) -> dict[tuple[str, int], dict[str, Any]]:
    result: dict[tuple[str, int], dict[str, Any]] = {}
    priority = {"standard": 2, "first_unit": 1, "subsequent_unit": 0}
    for record in load(project, "points").get("points", []):
        key = (record["unit_id"], record["unit_size"])
        if key not in result or priority.get(record.get("cost_tier"), -1) > priority.get(result[key].get("cost_tier"), -1):
            result[key] = record
    return result


def evaluate_list(project: Path, army: dict[str, Any]) -> dict[str, Any]:
    owned = {item["unit_id"]: item["quantity_owned"] for item in load(project, "collection").get("collection", [])}
    points = latest_points(project)
    missing: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    total = 0
    for selection in army.get("units", []):
        unit_id, quantity = selection["unit_id"], selection["quantity"]
        available = owned.get(unit_id, 0)
        if quantity > available:
            missing.append({"unit_id": unit_id, "required": quantity, "owned": available, "missing": quantity - available})
        unit_size = selection.get("unit_size", quantity)
        record = points.get((unit_id, unit_size))
        if record is None:
            stale.append({"unit_id": unit_id, "unit_size": unit_size, "reason": "no verified points"})
        else:
            total += record["value"]
    return {"list_id": army.get("id"), "total_points": total if not stale else None, "missing": missing, "points_requiring_verification": stale, "valid": not missing and not stale}


def list_status(project: Path, list_id: str | None) -> list[dict[str, Any]]:
    armies = load(project, "lists").get("lists", [])
    selected = [army for army in armies if list_id is None or army.get("id") == list_id]
    if list_id and not selected:
        raise ValueError(f"Unknown army list: {list_id}")
    return [evaluate_list(project, army) for army in selected]


def collection_points(project: Path) -> dict[str, Any]:
    points = latest_points(project)
    total = 0
    uncertain = []
    for item in load(project, "collection").get("collection", []):
        owned = item["quantity_owned"]
        options = [(size, record["value"]) for (unit_id, size), record in points.items() if unit_id == item["unit_id"] and size <= owned]
        totals: list[int | None] = [0] + [None] * owned
        for quantity in range(1, owned + 1):
            values = [totals[quantity - size] + value for size, value in options if size <= quantity and totals[quantity - size] is not None]
            totals[quantity] = max(values) if values else None
        if owned and totals[owned] is not None:
            total += totals[owned]
        elif owned:
            uncertain.append({"unit_id": item["unit_id"], "quantity_owned": owned, "reason": "no verified points for owned quantity"})
    return {"verified_total_points": total, "complete": not uncertain, "points_requiring_verification": uncertain}


def reconcile(project: Path, supplied_path: Path, apply: bool) -> dict[str, Any]:
    canonical = load(project, "collection")
    supplied_data = yaml.safe_load(supplied_path.read_text(encoding="utf-8")) or {}
    supplied = supplied_data.get("collection", supplied_data if isinstance(supplied_data, list) else [])
    old = keyed(canonical.get("collection", []))
    new = keyed(supplied)
    additions = [new[key] for key in new.keys() - old.keys()]
    removals = [old[key] for key in old.keys() - new.keys()]
    differences = []
    uncertain = []
    for key in old.keys() & new.keys():
        changes = {field: {"canonical": old[key].get(field), "provided": new[key].get(field)} for field in set(old[key]) | set(new[key]) if old[key].get(field) != new[key].get(field)}
        if changes:
            differences.append({"unit_id": key, "changes": changes})
    for item in supplied:
        for field in ("quantity_owned", "quantity_assembled", "quantity_painted"):
            if item.get(field) is None:
                uncertain.append({"unit_id": item.get("unit_id"), "field": field})
    report = {"additions": additions, "removals": removals, "differences": differences, "uncertain": uncertain, "applied": False}
    if apply:
        if uncertain:
            raise ValueError("Cannot apply reconciliation with uncertain required quantities")
        updated = copy.deepcopy(canonical)
        updated["collection"] = supplied
        updated["baseline_confirmed"] = True
        updated["last_reconciled"] = date.today().isoformat()
        save(project, "collection", updated)
        report["applied"] = True
        report["collection_points"] = collection_points(project)
        report["list_validation"] = list_status(project, None)
    return report


def receive(project: Path, unit_id: str, quantity: int) -> dict[str, Any]:
    collection = load(project, "collection")
    purchases = load(project, "purchases")
    plan = next((item for item in purchases.get("purchases", []) if item["unit_id"] == unit_id), None)
    if plan is None or plan.get("status") != "ordered":
        raise ValueError("A receipt requires a matching ordered purchase")
    if quantity > plan["quantity"]:
        raise ValueError("Received quantity exceeds ordered quantity")
    item = next((item for item in collection.get("collection", []) if item["unit_id"] == unit_id), None)
    if item is None:
        item = {"unit_id": unit_id, "unit": plan["unit"], "quantity_owned": 0, "quantity_assembled": 0, "quantity_painted": 0, "statuses": ["owned"], "paint_scheme_ref": plan.get("paint_scheme_ref"), "energy_scheme": plan.get("energy_scheme"), "build_configuration": None, "storage_location_ref": None, "notes": None}
        collection.setdefault("collection", []).append(item)
    item["quantity_owned"] += quantity
    item["statuses"] = sorted(set(item.get("statuses", [])) | {"owned"})
    plan["quantity"] -= quantity
    plan["status"] = "received" if plan["quantity"] == 0 else "ordered"
    plan["received_date"] = date.today().isoformat()
    save(project, "collection", collection)
    save(project, "purchases", purchases)
    return {"unit_id": unit_id, "quantity_received": quantity, "quantity_owned": item["quantity_owned"], "purchase_status": plan["status"], "collection_points": collection_points(project), "list_validation": list_status(project, None)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a structured Warhammer 40,000 collection")
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("points")
    status = sub.add_parser("list-status")
    status.add_argument("--list-id")
    rec = sub.add_parser("reconcile")
    rec.add_argument("--input", type=Path, required=True)
    rec.add_argument("--apply", action="store_true")
    received = sub.add_parser("receive")
    received.add_argument("unit_id")
    received.add_argument("quantity", type=int)
    args = parser.parse_args()
    try:
        project = args.project.resolve()
        if args.command == "validate":
            result: Any = {"valid": not (errors := validate(project)), "errors": errors}
        elif args.command == "points":
            result = collection_points(project)
        elif args.command == "list-status":
            result = list_status(project, args.list_id)
        elif args.command == "reconcile":
            result = reconcile(project, args.input, args.apply)
        else:
            result = receive(project, args.unit_id, args.quantity)
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
        return 0 if not isinstance(result, dict) or result.get("valid", True) else 1
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
