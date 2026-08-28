#!/usr/bin/env python3
"""
Deterministic tests for Cross-Domain Reasoning.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))

from context_assembly import assemble
from cross_domain_reasoning import reason
from universal_retrieval import build_retriever


def _bundle_for(intent: str, query: str, desired_depth: str = "deep", entity_refs=None):
    return assemble(
        {
            "intent": intent,
            "query": query,
            "domains": ["planning", "knowledge", "career"],
            "avoid_domains": ["health", "finance", "music"],
            "desired_depth": desired_depth,
            "entity_refs": entity_refs or [],
        },
        demo_only=True,
    )


def test_explicit_relationship_connection():
    print("A. Explicit relationship connection")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, focal_id="goal-ai-engineering", modes=["connection"])
    assert any(f["type"] == "connection" and "goal-ai-engineering" in f["object_ids"] for f in findings)
    print("  PASS")


def test_transfer_opportunity():
    print("B. Transfer opportunity")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, modes=["transfer_opportunity"], limit=20)
    types = {f["type"] for f in findings}
    assert "transfer_opportunity" in types
    assert any("lp-agentic-ai-linkedin" in f["object_ids"] for f in findings if f["type"] == "transfer_opportunity")
    print("  PASS")


def test_gap():
    print("C. Gap")
    bundle = _bundle_for("goal-review", "AI engineering")
    findings = reason(bundle, focal_id="goal-ai-engineering", modes=["gap", "evidence_gap"], limit=20)
    gap_types = {f["type"] for f in findings}
    assert "evidence_gap" in gap_types or "gap" in gap_types
    print("  PASS")


def test_conflict():
    print("D. Conflict/tradeoff")
    bundle = _bundle_for("course-decision", "agent evaluation", entity_refs=["demo-baseline-schedule"])
    findings = reason(bundle, modes=["conflict", "tradeoff"], limit=20)
    types = {f["type"] for f in findings}
    assert "tradeoff" in types or "conflict" in types
    print("  PASS")


def test_overlap():
    print("E. Overlap")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, modes=["overlap"], limit=20)
    types = {f["type"] for f in findings}
    assert "overlap" in types
    print("  PASS")


def test_priority_mismatch():
    print("F. Priority mismatch")
    bundle = _bundle_for("goal-review", "explore new domain", entity_refs=["goal-explore-new-domain"])
    findings = reason(bundle, focal_id="goal-explore-new-domain", modes=["priority_mismatch"], limit=20)
    types = {f["type"] for f in findings}
    assert "priority_mismatch" in types
    print("  PASS")


def test_why_trace():
    print("G. Why trace")
    bundle = _bundle_for("goal-review", "AI engineering", entity_refs=["task-implement-control-loop"])
    findings = reason(bundle, focal_id="task-implement-control-loop", modes=["connection"], limit=50)
    # Should trace task → project → goal.
    chain = next((f for f in findings if f["type"] == "connection" and "task-implement-control-loop" in f["object_ids"] and "goal-ai-engineering" in f["object_ids"]), None)
    assert chain is not None
    print("  PASS")


def test_reverse_trace():
    print("H. Reverse trace / what supports goal")
    bundle = _bundle_for("goal-review", "AI engineering")
    findings = reason(bundle, focal_id="goal-ai-engineering", modes=["connection"], limit=20)
    support = next((f for f in findings if f["type"] == "connection" and f["object_ids"][0] == "goal-ai-engineering"), None)
    assert support is not None
    print("  PASS")


def test_provenance():
    print("I. Provenance")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, modes=["connection"], limit=5)
    for f in findings:
        assert "evidence" in f
        assert "object_ids" in f and f["object_ids"]
    print("  PASS")


def test_excluded_domains():
    print("J. Excluded domains")
    bundle = _bundle_for("course-decision", "agent evaluation", entity_refs=["lp-agentic-ai-linkedin"])
    assert "health" not in {d for d in bundle.get("current_state", []) for d in d.get("domain", [])}  # noqa: not exact
    findings = reason(bundle, modes=["connection", "transfer_opportunity", "overlap", "gap"], limit=20)
    for f in findings:
        assert "health" not in f.get("domains", [])
        assert "finance" not in f.get("domains", [])
        assert "music" not in f.get("domains", [])
    print("  PASS")


def test_unsupported_inference():
    print("K. Unsupported inference")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, modes=["connection", "transfer_opportunity", "gap", "overlap", "priority_mismatch", "tradeoff"], limit=20)
    for f in findings:
        # Every material finding refers to objects in the bundle.
        assert f["object_ids"]
        for oid in f["object_ids"]:
            assert oid in [i["object_id"] for i in bundle["current_state"] + bundle["relevant_history"] + bundle["related_knowledge"] + bundle["active_constraints"]]
    print("  PASS")


def test_unresolved_explicit_reference():
    print("L. Explicit missing entity_ref")
    bundle = _bundle_for("course-decision", "agent evaluation", entity_refs=["missing-object-123"])
    assert "missing-object-123" in bundle.get("unresolved_refs", [])
    print("  PASS")


def test_boundedness():
    print("M. Boundedness")
    bundle = _bundle_for("course-decision", "agent evaluation")
    findings = reason(bundle, limit=7)
    assert len(findings) <= 7
    print("  PASS")


def main():
    print("Cross-Domain Reasoning deterministic tests")
    print("=" * 42)
    test_explicit_relationship_connection()
    test_transfer_opportunity()
    test_gap()
    test_conflict()
    test_overlap()
    test_priority_mismatch()
    test_why_trace()
    test_reverse_trace()
    test_provenance()
    test_excluded_domains()
    test_unsupported_inference()
    test_unresolved_explicit_reference()
    test_boundedness()
    print("\nAll Cross-Domain Reasoning tests passed.")


if __name__ == "__main__":
    main()
