#!/usr/bin/env python3
"""
Deterministic tests for Decision Intelligence, Review Orchestrator, and Goal Review.
"""

import sys
import yaml
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))

from context_assembly import assemble
from cross_domain_reasoning import reason
from review_orchestrator import orchestrate
from universal_retrieval import build_retriever


def _bundle_for(query: str, domains=None, entity_refs=None):
    return assemble(
        {
            "intent": "sunday-review",
            "query": query,
            "domains": domains or ["planning", "knowledge", "career"],
            "avoid_domains": ["health", "finance", "music"],
            "desired_depth": "deep",
            "entity_refs": entity_refs or [],
        },
        demo_only=True,
    )


def test_decision_schema_registered():
    print("A. Decision schema registered")
    registry_path = Path(__file__).resolve().parent.parent / "schemas" / "registry.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    assert "knowledge.decision" in registry.get("schemas", {})
    print("  PASS")


def test_decision_fixture_parses():
    print("B. Decision fixture parses")
    r = build_retriever(demo_only=True)
    obj = r.get_object("decision-agent-course")
    assert obj is not None
    assert obj["schema"] == "knowledge.decision"
    assert obj["status"] == "active"
    assert "reasoning" in obj
    print("  PASS")


def test_decision_goal_link():
    print("C. Decision -> goal link")
    r = build_retriever(demo_only=True)
    obj = r.get_object("decision-agent-course")
    assert "goal-ai-engineering" in obj.get("related_goal_ids", [])
    print("  PASS")


def test_decision_expected_vs_actual_distinct():
    print("D. Expected vs actual outcome distinct")
    r = build_retriever(demo_only=True)
    obj = r.get_object("decision-agent-course")
    assert obj.get("expected_outcomes")
    # actual_outcome is not yet set in fixture.
    assert obj.get("actual_outcome", "") == ""
    print("  PASS")


def test_decision_review_date_detection():
    print("E. Decision review date detection")
    bundle = _bundle_for("", entity_refs=["decision-agent-course"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    ids = {r["object_id"] for r in plan["recommendations"]}
    assert "decision-agent-course" in ids
    print("  PASS")


def test_decision_not_due():
    print("F. Decision not due yet")
    bundle = _bundle_for("", entity_refs=["decision-agent-course"])
    plan = orchestrate(bundle, current_date=date(2026, 2, 15))
    ids = {r["object_id"] for r in plan["recommendations"]}
    assert "decision-agent-course" not in ids
    print("  PASS")


def test_cross_domain_reasoning_decision_support():
    print("G. Cross-domain reasoning recognizes decision support")
    bundle = _bundle_for("", entity_refs=["decision-agent-course"])
    findings = reason(bundle, focal_id="goal-ai-engineering", modes=["connection"], limit=20)
    ids = {oid for f in findings for oid in f["object_ids"]}
    assert "decision-agent-course" in ids
    print("  PASS")


def test_orchestrator_skips_empty_domain():
    print("H. Orchestrator skips empty domain")
    bundle = _bundle_for("")
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    skipped_types = {s["review_type"] for s in plan["skipped"]}
    assert "finance-review" in skipped_types
    print("  PASS")


def test_orchestrator_assessment_approaching():
    print("I. Orchestrator surfaces approaching assessment")
    bundle = _bundle_for("", entity_refs=["lp-agentic-ai-linkedin"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    types = {r["review_type"] for r in plan["recommendations"]}
    assert "learning-review" in types
    print("  PASS")


def test_orchestrator_goal_mismatch():
    print("J. Orchestrator surfaces goal mismatch")
    bundle = _bundle_for("", entity_refs=["goal-explore-new-domain"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    ids = {r["object_id"] for r in plan["recommendations"]}
    assert "goal-explore-new-domain" in ids
    print("  PASS")


def test_orchestrator_retention_due():
    print("K. Orchestrator surfaces due retention review")
    bundle = _bundle_for("", entity_refs=["rev-20260115-001"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    ids = {r["object_id"] for r in plan["recommendations"]}
    assert "rev-20260115-001" in ids
    print("  PASS")


def test_orchestrator_bounded():
    print("L. Orchestrator bounded")
    bundle = _bundle_for("")
    plan = orchestrate(bundle, current_date=date(2026, 8, 28), max_recommendations=3)
    assert len(plan["recommendations"]) <= 3
    print("  PASS")


def test_orchestrator_delegation():
    print("M. Orchestrator delegates to workflows")
    bundle = _bundle_for("", entity_refs=["decision-agent-course"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    for rec in plan["recommendations"]:
        assert "delegated_workflow" in rec and rec["delegated_workflow"]
    print("  PASS")


def test_orchestrator_provenance():
    print("N. Orchestrator provenance")
    bundle = _bundle_for("", entity_refs=["decision-agent-course"])
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    assert "provenance" in plan
    print("  PASS")


def test_goal_review_activity_and_outcome():
    print("O. Goal review distinguishes activity and outcome")
    bundle = _bundle_for("", entity_refs=["goal-ai-engineering"])
    findings = reason(bundle, focal_id="goal-ai-engineering", limit=20)
    # Should find supporting activity (connection).
    support = [f for f in findings if f["type"] == "connection" and f["object_ids"][0] == "goal-ai-engineering"]
    assert support
    # No fake percentage outcome.
    for f in findings:
        assert "%" not in f["statement"]
    # A goal with no execution should show an execution/mismatch finding.
    bundle_empty = _bundle_for("", entity_refs=["goal-explore-new-domain"])
    findings_empty = reason(bundle_empty, focal_id="goal-explore-new-domain", limit=20)
    gap = [f for f in findings_empty if f["type"] in ("gap", "evidence_gap", "priority_mismatch") and "goal-explore-new-domain" in f["object_ids"]]
    assert gap
    print("  PASS")


def test_goal_review_conflicting_commitments():
    print("P. Goal review surfaces conflicting commitments")
    bundle = _bundle_for("", entity_refs=["demo-baseline-schedule", "lp-agentic-ai-linkedin", "lp-ai-agents-udemy"])
    findings = reason(bundle, modes=["tradeoff"], limit=10)
    types = {f["type"] for f in findings}
    assert "tradeoff" in types
    print("  PASS")


def test_goal_review_historical_not_current():
    print("Q. Historical/superseded not treated as current")
    # decision-agent-course is active; check no completed or superseded decision is promoted.
    r = build_retriever(demo_only=True)
    obj = r.get_object("decision-agent-course")
    assert obj["status"] != "completed"
    assert obj["status"] != "superseded"
    print("  PASS")


def main():
    print("Decision Intelligence + Review Orchestrator tests")
    print("=" * 48)
    test_decision_schema_registered()
    test_decision_fixture_parses()
    test_decision_goal_link()
    test_decision_expected_vs_actual_distinct()
    test_decision_review_date_detection()
    test_decision_not_due()
    test_cross_domain_reasoning_decision_support()
    test_orchestrator_skips_empty_domain()
    test_orchestrator_assessment_approaching()
    test_orchestrator_goal_mismatch()
    test_orchestrator_retention_due()
    test_orchestrator_bounded()
    test_orchestrator_delegation()
    test_orchestrator_provenance()
    test_goal_review_activity_and_outcome()
    test_goal_review_conflicting_commitments()
    test_goal_review_historical_not_current()
    print("\nAll Decision + Review tests passed.")


if __name__ == "__main__":
    main()
