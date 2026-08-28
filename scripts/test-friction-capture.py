#!/usr/bin/env python3
"""
Deterministic tests for Beta friction / usage feedback capture.
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))

import friction_log as fl


ROOT = Path(__file__).resolve().parent.parent
DEMO_FRICTION_ROOT = ROOT / "config" / "demo-personality" / "fixtures" / "domains" / "system" / "friction"
ETHAN_LIFE_FRICTION = ROOT.parent / "ethan-life" / "domains" / "system" / "friction"
REGISTRY = ROOT / "schemas" / "registry.yaml"


def _new_temp_root():
    return Path(tempfile.mkdtemp(prefix="friction-test-"))


def test_schema_registered():
    print("A. Friction log schema registered")
    import yaml
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert "core.friction-log" in registry.get("schemas", {}), "schema not in registry"
    entry = registry["schemas"]["core.friction-log"]
    assert entry.get("file") == "core/friction-log.schema.yaml"
    print("  PASS")


def test_single_statement_capture_is_valid():
    print("B. Single-statement capture produces a valid friction entry")
    root = _new_temp_root()
    entry = fl.prepare_friction_entry(
        "That was annoying; you asked me something you already knew.",
        expected="Use the active reading state.",
        observed="Asked which book I am reading.",
        context={"current_workflow": "workflows/knowledge/start-reading.md", "current_capability": "Guided Reading"},
    )
    saved, _ = fl.create_or_update_friction_entry(root, entry)
    assert saved["schema"] == "core.friction-log"
    assert saved["status"] == "open"
    assert saved["user_expectation"] == "Use the active reading state."
    assert saved["observed_behavior"] == "Asked which book I am reading."
    assert saved["affected_workflow"] == "workflows/knowledge/start-reading.md"
    assert saved["affected_capability"] == "Guided Reading"
    assert saved["feedback_type"] == "asked_known_information"
    print("  PASS")


def test_workflow_inferred_from_context():
    print("C. Known workflow inferred from context")
    entry = fl.prepare_friction_entry("That was wrong.", context={"current_workflow": "workflows/core/ask.md"})
    assert entry["affected_workflow"] == "workflows/core/ask.md"
    print("  PASS")


def test_expected_vs_observed_preserved():
    print("D. Expected vs observed preserved in fixture")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    e = entries["friction-demo-asked-known-001"]
    assert e["user_expectation"] and e["observed_behavior"]
    assert e["user_expectation"] != e["observed_behavior"]
    print("  PASS")


def test_duplicate_updates_occurrence():
    print("E. Duplicate issue increments occurrence_count, not uncontrolled duplication")
    root = _new_temp_root()
    first = {
        "id": "friction-test-duplicate-001",
        "schema": "core.friction-log",
        "schema_version": 1,
        "title": "Duplicate test",
        "created_at": "2026-08-27",
        "updated_at": "2026-08-27",
        "status": "open",
        "summary": "Sunday planning asks too many questions",
        "feedback_type": "excessive_questions",
        "affected_capability": "Planning / Weekly Review",
        "affected_workflow": "workflows/planning/weekly-review.md",
        "severity": "medium",
        "occurrence_count": 1,
        "occurrence_dates": ["2026-08-27"],
        "provenance": {"agent_version": "ethan-os-0.1.0", "provenance_note": "test"},
    }
    fl.create_or_update_friction_entry(root, first)
    second = first.copy()
    second["occurrence_context_refs"] = ["bundle-20260827-002"]
    saved, created = fl.create_or_update_friction_entry(root, second)
    assert not created
    assert saved["occurrence_count"] == 2
    assert "bundle-20260827-002" in saved.get("occurrence_context_refs", [])
    # should still be exactly one file with this id
    files = [p for p in root.rglob("*.md") if p.name != "README.md"]
    assert len(files) == 1
    print("  PASS")


def test_context_refs_preserved():
    print("F. Context refs preserved in capture")
    root = _new_temp_root()
    entry = fl.prepare_friction_entry(
        "That pulled the wrong context.",
        context={"context_refs": ["bundle-20260827-005", "book-ai-engineering"]},
    )
    saved, _ = fl.create_or_update_friction_entry(root, entry)
    assert "bundle-20260827-005" in saved["context_refs"]
    assert "book-ai-engineering" in saved["context_refs"]
    print("  PASS")


def test_private_storage_is_ethan_life():
    print("G. Private friction storage is in ethan-life, not ethan-os")
    assert ETHAN_LIFE_FRICTION.exists(), "ethan-life friction dir missing"
    # The canonical schema and demo fixtures live in ethan-os; actual entries belong in ethan-life.
    assert not str(ETHAN_LIFE_FRICTION).startswith(str(ROOT)), "ethan-life friction path is inside ethan-os"
    print("  PASS")


def test_review_groups_repeated_issues():
    print("H. Review groups repeated issues")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    groups = fl.group_friction(entries)
    assert len(groups["repeated"]) > 0, "no repeated issues found"
    assert len(groups["by_feedback_type"]) > 0
    assert len(groups["by_root_cause"]) > 0
    print("  PASS")


def test_resolved_excluded_from_open_view():
    print("I. Resolved issues excluded from default open view")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    open_items = fl.top_open_friction(entries, n=10)
    open_ids = {e["id"] for e in open_items}
    assert "friction-demo-generic-rec-003" not in open_ids, "resolved item appeared in open view"
    print("  PASS")


def test_high_severity_before_low():
    print("J. High-severity issues surfaced before low-severity noise")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    open_items = fl.top_open_friction(entries, n=10)
    severities = [e.get("severity") for e in open_items]
    # The high-severity wrong-context should appear before the low positive signal if both are open.
    high_index = next((i for i, s in enumerate(severities) if s == "high"), None)
    low_index = next((i for i, s in enumerate(severities) if s == "low"), None)
    if high_index is not None and low_index is not None:
        assert high_index < low_index
    print("  PASS")


def test_friction_to_evaluation_candidate():
    print("K. Friction can convert to an evaluation candidate")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    e = entries["friction-demo-asked-known-001"]
    expectation = fl.suggest_evaluation_expectation(e)
    assert expectation and "should" in expectation
    print("  PASS")


def test_positive_feedback_captured():
    print("L. Positive feedback captured")
    entries = fl.load_friction_entries(DEMO_FRICTION_ROOT)
    positives = [e for e in entries.values() if e.get("is_positive")]
    assert positives, "no positive feedback fixture found"
    assert positives[0].get("feedback_type") == "worked_well"
    print("  PASS")


def main():
    print("Friction / usage-feedback tests")
    print("=" * 40)
    test_schema_registered()
    test_single_statement_capture_is_valid()
    test_workflow_inferred_from_context()
    test_expected_vs_observed_preserved()
    test_duplicate_updates_occurrence()
    test_context_refs_preserved()
    test_private_storage_is_ethan_life()
    test_review_groups_repeated_issues()
    test_resolved_excluded_from_open_view()
    test_high_severity_before_low()
    test_friction_to_evaluation_candidate()
    test_positive_feedback_captured()
    print("\nAll friction tests passed.")


if __name__ == "__main__":
    main()
