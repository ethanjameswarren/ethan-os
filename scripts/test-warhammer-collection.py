#!/usr/bin/env python3

import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hobby"))
from warhammer_collection import collection_points, evaluate_list, receive, reconcile, validate


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        dump(project / "collection/inventory.yaml", {"baseline_confirmed": True, "collection": [{"unit_id": "warriors", "unit": "Necron Warriors", "quantity_owned": 10, "quantity_assembled": 10, "quantity_painted": 5, "statuses": ["owned"], "paint_scheme_ref": "dynasty-standard", "energy_scheme": "cyan"}]})
        dump(project / "rules/points/current.yaml", {"source": {"provider": "Games Workshop", "publication": "MFM", "version": "1.4", "retrieved_at": "2026-09-19", "last_verified_at": "2026-09-19"}, "points": [{"unit_id": "warriors", "value": 100, "unit_size": 10, "cost_tier": "standard"}]})
        dump(project / "army-lists/lists.yaml", {"lists": [{"id": "test", "units": [{"unit_id": "warriors", "quantity": 20, "unit_size": 10}]}]})
        dump(project / "purchases/plan.yaml", {"purchases": [{"unit_id": "wraiths", "unit": "Canoptek Wraiths", "quantity": 6, "status": "ordered", "paint_scheme_ref": "dynasty-standard", "energy_scheme": "cyan"}]})
        dump(project / "storage/locations.yaml", {"locations": []})
        dump(project / "painting/scheme-references.yaml", {"dynasty_paint_scheme": {"id": "dynasty-standard", "energy_classes": {"cyan": {}, "red": {}, "purple": {}}}})

        assert validate(project) == []
        assert collection_points(project)["verified_total_points"] == 100
        result = evaluate_list(project, {"id": "test", "units": [{"unit_id": "warriors", "quantity": 20, "unit_size": 10}]})
        assert result["missing"][0]["missing"] == 10
        supplied = project / "supplied.yaml"
        dump(supplied, {"collection": [{"unit_id": "warriors", "unit": "Necron Warriors", "quantity_owned": 20, "quantity_assembled": 10, "quantity_painted": 5, "statuses": ["owned"], "paint_scheme_ref": "dynasty-standard", "energy_scheme": "cyan"}]})
        preview = reconcile(project, supplied, False)
        assert preview["differences"] and not preview["applied"]
        applied = reconcile(project, supplied, True)
        assert applied["applied"]
        receipt = receive(project, "wraiths", 6)
        assert receipt["quantity_owned"] == 6 and receipt["purchase_status"] == "received"

    print("Warhammer collection tests passed.")


if __name__ == "__main__":
    main()
