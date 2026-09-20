#!/usr/bin/env python3

import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hobby"))
from warhammer_rules import differences, required_units, validate


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        dump(project / "collection/inventory.yaml", {"collection": [{"unit_id": "owned", "unit": "Owned", "quantity_owned": 1}]})
        dump(project / "purchases/plan.yaml", {"purchases": [{"unit_id": "planned", "unit": "Planned", "quantity": 1, "status": "planned"}]})
        base = {"schema": "hobby.warhammer-datasheet", "unit_id": "", "unit": "", "faction": "Test", "edition": 11, "source": {"provider": "Wahapedia", "url": "https://example.test", "faction_pack_version": "1.0", "source_last_updated": "2026-09", "retrieved_at": "2026-09-19", "last_verified_at": "2026-09-19"}, "profile": {}, "ranged_weapons": [], "melee_weapons": [], "core_abilities": [], "army_rules": [], "unit_abilities": [], "keywords": [], "faction_keywords": [], "change_history": []}
        for unit_id in ("owned", "planned"):
            sheet = dict(base, unit_id=unit_id, unit=unit_id.title())
            dump(project / "rules/datasheets" / f"{unit_id}.yaml", sheet)
        dump(project / "rules/points/current.yaml", {"points": [{"unit_id": "owned"}, {"unit_id": "planned"}]})
        assert set(required_units(project)) == {"owned", "planned"}
        assert validate(project) == []
        assert differences({"profile": {"toughness": 5}}, {"profile": {"toughness": 6}}) == [{"field": "profile.toughness", "previous": 5, "new": 6}]
        assert differences({"source": {"last_verified_at": "old"}}, {"source": {"last_verified_at": "new"}}) == []
    print("Warhammer rules tests passed.")


if __name__ == "__main__":
    main()
