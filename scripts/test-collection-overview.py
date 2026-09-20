#!/usr/bin/env python3

import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hobby"))
from generate_collection_overview import points_for_quantity, render, summarize


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        dump(project / "collection/inventory.yaml", {"collection": [
            {"unit_id": "warriors", "unit": "Warriors", "collection_group": "Infantry", "quantity_owned": 20, "quantity_assembled": 20, "quantity_painted": 3, "energy_scheme": "cyan"},
            {"unit_id": "destroyers", "unit": "Destroyers", "collection_group": "Destroyers", "quantity_owned": 6, "quantity_assembled": 6, "quantity_painted": 6, "energy_scheme": "red"},
        ]})
        dump(project / "rules/points/current.yaml", {"verification_status": "verified", "source": {"version": "1.4", "last_verified_at": "2026-09-19"}, "points": [
            {"unit_id": "warriors", "unit_size": 10, "value": 90, "verified_date": "2026-01-01"},
            {"unit_id": "warriors", "unit_size": 10, "value": 100, "verified_date": "2026-09-01"},
            {"unit_id": "destroyers", "unit_size": 3, "value": 100, "verified_date": "2026-09-02"},
            {"unit_id": "wraiths", "unit_size": 3, "value": 110, "verified_date": "2026-09-03"},
        ]})
        dump(project / "purchases/plan.yaml", {"purchases": [{"unit_id": "wraiths", "unit": "Wraiths", "quantity": 6, "status": "planned", "priority": "high", "strategic_reason": "Mobility", "energy_scheme": "cyan"}]})
        dump(project / "army-lists/lists.yaml", {"lists": [
            {"id": "ready", "name": "Ready", "target_points": 200, "units": [{"unit_id": "destroyers", "quantity": 6, "unit_size": 6}]},
            {"id": "missing", "name": "Missing", "target_points": 220, "units": [{"unit_id": "wraiths", "quantity": 6, "unit_size": 6}]},
            {"id": "draft", "name": "Draft", "target_points": 2000, "units": []},
        ]})
        dump(project / "painting/scheme-references.yaml", {"dynasty_paint_scheme": {"id": "dynasty-standard"}})

        summary = summarize(project)
        assert summary["model_count"] == 26
        assert summary["unit_types"] == 2
        assert summary["assembled"] == 26 and summary["painted"] == 9 and summary["remaining"] == 17
        assert summary["owned_points"] == 400
        assert summary["planned_points"] == 220 and summary["projected_points"] == 620
        assert summary["last_points_verification"] == "2026-09-19"
        assert [concept["status"] for concept in summary["concepts"]] == ["READY", "MISSING MODELS", "DRAFT"]
        assert points_for_quantity("warriors", 20, {("warriors", 10): {"value": 100}}) == 200
        page = render(summary)
        assert "26 Models" in page and "9 / 26" in page and "MISSING MODELS" in page

    print("Collection overview tests passed.")


if __name__ == "__main__":
    main()
