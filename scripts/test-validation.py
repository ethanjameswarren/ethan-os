#!/usr/bin/env python3

import importlib.util
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "validate.py"
SPEC = importlib.util.spec_from_file_location("ethan_validate", SCRIPT)
VALIDATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE)


def test_dangling_internal_link_fails():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        obj = root / "object.md"
        obj.write_text(
            "---\nid: object-1\nschema: test\nschema_version: 1\ntitle: Test\ncreated_at: 2026-08-31\n"
            "links:\n  - target: missing-object\n    relation: related_to\n"
            "provenance:\n  agent_version: ethan-os/0.1.1-beta\n  provenance_note: test\n---\n",
            encoding="utf-8",
        )
        previous_root = VALIDATE.ETHAN_LIFE
        VALIDATE.ETHAN_LIFE = root
        try:
            broken = []
            VALIDATE.validate_relationship_targets([obj], {"object-1": "object.md"}, broken)
        finally:
            VALIDATE.ETHAN_LIFE = previous_root
        assert broken == ["object.md: broken link to unknown id 'missing-object'"]


def test_external_provenance_is_not_an_internal_link():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        obj = root / "object.md"
        obj.write_text(
            "---\nid: object-1\nschema: test\nschema_version: 1\ntitle: Test\ncreated_at: 2026-08-31\n"
            "provenance:\n  agent_version: ethan-os/0.1.1-beta\n  provenance_note: test\n"
            "  source_id: external-user-summary\n---\n",
            encoding="utf-8",
        )
        previous_root = VALIDATE.ETHAN_LIFE
        VALIDATE.ETHAN_LIFE = root
        try:
            broken = []
            VALIDATE.validate_relationship_targets([obj], {"object-1": "object.md"}, broken)
        finally:
            VALIDATE.ETHAN_LIFE = previous_root
        assert broken == []


if __name__ == "__main__":
    test_dangling_internal_link_fails()
    test_external_provenance_is_not_an_internal_link()
    print("Validation integrity tests passed.")
