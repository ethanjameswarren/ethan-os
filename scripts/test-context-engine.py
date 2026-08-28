#!/usr/bin/env python3
"""
Deterministic tests for the Context Engine and Universal Personal Retrieval.

Uses demo fixtures only, no real ethan-life state.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))

from context_assembly import assemble
from universal_retrieval import UniversalRetriever, build_retriever


def _ids(items):
    return {i["object_id"] for i in items}


def _contains(items, obj_id):
    return any(i["object_id"] == obj_id for i in items)


def test_explicit_reference():
    print("A. Explicit reference retrieval")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="", entity_refs=["lp-agentic-ai-linkedin"], top_k=5)["results"]
    assert any(res["object_id"] == "lp-agentic-ai-linkedin" for res in results)
    print("  PASS")


def test_cross_domain_retrieval():
    print("B. Cross-domain retrieval")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="agent evaluation", domains=["knowledge", "planning", "career"], top_k=10)["results"]
    ids = {res["object_id"] for res in results}
    assert "project-agent-eval-prototype" in ids
    assert "idea-agent-evaluation" in ids
    assert "lp-agentic-ai-linkedin" in ids or "evidence-ai-project-lead" in ids
    print("  PASS")


def test_domain_filtering():
    print("C. Domain filtering")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="agent", avoid_domains=["career"], top_k=20)["results"]
    assert all(res["domain"] != "career" for res in results)
    print("  PASS")


def test_current_state_preference():
    print("D. Current-state preference")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="agent evaluation", top_k=5, statuses=["active", "in_progress", "reading", "learning"])["results"]
    ids = {res["object_id"] for res in results}
    # The active learning program or active project should rank.
    assert any(res["status"] in ("active", "in_progress", "reading", "learning") for res in results)
    print("  PASS")


def test_relationship_traversal():
    print("E. Relationship traversal")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="AI engineering", top_k=10, depth="deep")["results"]
    ids = {res["object_id"] for res in results}
    # Direct + one-hop should bring in linked project/learning/career.
    assert "goal-ai-engineering" in ids
    assert "project-agent-eval-prototype" in ids
    assert "job-target-ai-engineering" in ids or "lp-agentic-ai-linkedin" in ids
    print("  PASS")


def test_light_context():
    print("F. Light context")
    bundle = assemble(
        {
            "intent": "course-decision",
            "query": "agent evaluation",
            "domains": ["planning", "knowledge", "career"],
            "desired_depth": "light",
            "avoid_domains": ["health", "finance", "music"],
        },
        demo_only=True,
    )
    total = len(bundle["current_state"]) + len(bundle["related_knowledge"]) + len(bundle["relevant_history"])
    assert total <= 5, f"Light context returned {total} items"
    assert all(
        item.get("domain") not in ("health", "finance", "music")
        for item in bundle["current_state"] + bundle["related_knowledge"] + bundle["relevant_history"]
    )
    print("  PASS")


def test_deep_context():
    print("G. Deep context")
    bundle = assemble(
        {
            "intent": "course-decision",
            "query": "agent evaluation",
            "domains": ["planning", "knowledge", "career"],
            "desired_depth": "deep",
            "avoid_domains": ["health", "finance", "music"],
        },
        demo_only=True,
    )
    ids = _ids(bundle["current_state"] + bundle["related_knowledge"] + bundle["relevant_history"])
    assert "goal-ai-engineering" in ids
    assert "project-agent-eval-prototype" in ids
    assert "idea-agent-evaluation" in ids or "evidence-ai-project-lead" in ids
    total = len(ids)
    assert total > 5, f"Deep context returned only {total} items"
    assert total <= 30, f"Deep context returned too many items: {total}"
    print("  PASS")


def test_no_result_behavior():
    print("H. No-result behavior")
    r = build_retriever(demo_only=True)
    results = r.retrieve(query="quantum biology pottery", top_k=5)["results"]
    assert len(results) == 0
    print("  PASS")


def test_resume_context_excludes_unrelated():
    print("I. Resume context excludes unrelated domains")
    bundle = assemble(
        {
            "intent": "tailored-resume",
            "query": "AI engineering",
            "domains": ["career", "planning", "knowledge"],
            "avoid_domains": ["health", "finance", "music"],
            "desired_depth": "normal",
        },
        demo_only=True,
    )
    all_items = bundle["current_state"] + bundle["related_knowledge"] + bundle["relevant_history"]
    assert _contains(bundle["current_state"], "evidence-ai-project-lead") or _contains(bundle["current_state"], "job-target-ai-engineering")
    assert not any(i.get("domain") in ("health", "finance", "music") for i in all_items)
    print("  PASS")


def test_sunday_planning_context():
    print("J. Sunday Planning context")
    bundle = assemble(
        {
            "intent": "sunday-review",
            "query": "plan next week",
            "domains": ["planning", "knowledge"],
            "desired_depth": "normal",
        },
        demo_only=True,
    )
    ids = _ids(bundle["current_state"] + bundle["related_knowledge"])
    assert "goal-ai-engineering" in ids
    assert "project-agent-eval-prototype" in ids
    assert "lp-agentic-ai-linkedin" in ids or "task-implement-control-loop" in ids
    print("  PASS")


def test_course_decision_context():
    print("K. Course decision context")
    bundle = assemble(
        {
            "intent": "course-decision",
            "query": "Should I take this LinkedIn Learning course?",
            "domains": ["career", "planning", "knowledge"],
            "desired_depth": "normal",
            "avoid_domains": ["health", "finance", "music"],
        },
        demo_only=True,
    )
    ids = _ids(bundle["current_state"] + bundle["related_knowledge"])
    assert "goal-ai-engineering" in ids
    assert "lp-agentic-ai-linkedin" in ids or "project-agent-eval-prototype" in ids
    all_items = bundle["current_state"] + bundle["related_knowledge"] + bundle["relevant_history"]
    assert not any(i.get("domain") in ("health", "finance", "music") for i in all_items)
    print("  PASS")


def test_provenance():
    print("L. Provenance retained")
    bundle = assemble(
        {
            "intent": "course-decision",
            "query": "agent evaluation",
            "domains": ["planning", "knowledge"],
            "desired_depth": "light",
        },
        demo_only=True,
    )
    for item in bundle["current_state"]:
        assert "provenance" in item
        assert "source_path" in item["provenance"]
    assert "provenance" in bundle
    print("  PASS")


def main():
    print("Context Engine deterministic tests")
    print("=" * 40)
    test_explicit_reference()
    test_cross_domain_retrieval()
    test_domain_filtering()
    test_current_state_preference()
    test_relationship_traversal()
    test_light_context()
    test_deep_context()
    test_no_result_behavior()
    test_resume_context_excludes_unrelated()
    test_sunday_planning_context()
    test_course_decision_context()
    test_provenance()
    print("\nAll Context Engine tests passed.")


if __name__ == "__main__":
    main()
