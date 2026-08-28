#!/usr/bin/env python3
"""
Review Orchestrator for Ethan OS.

Decides what is worth reviewing right now, without running every possible domain review.
"""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from context_assembly import assemble
from cross_domain_reasoning import reason
from universal_retrieval import build_retriever


DEFAULT_MAX_RECOMMENDATIONS = 7


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _parse_date(value) -> date | None:
    if not value:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def _days_until(target: date, now: date) -> int | None:
    return (target - now).days if target else None


def orchestrate(
    bundle: dict,
    current_date: date | None = None,
    max_recommendations: int = DEFAULT_MAX_RECOMMENDATIONS,
    retriever=None,
) -> dict:
    """Return a shortlist of reviews worth running now."""
    now = current_date or _today()
    if retriever is None:
        retriever = build_retriever(demo_only=True)
    recommendations = []
    skipped = []

    # Use cross-domain reasoning to find priority mismatches and conflicts.
    try:
        findings = reason(bundle, limit=15)
    except Exception:
        findings = []

    # 1. Decision reviews.
    decisions = [
        item for item in bundle.get("current_state", []) + bundle.get("relevant_history", [])
        if item.get("object_schema") == "knowledge.decision"
    ]
    if not decisions:
        skipped.append({"review_type": "decision-review", "reason": "no decisions in context"})
    for item in decisions:
        obj = retriever.get_object(item["object_id"])
        review = _parse_date(obj.get("review_date")) if obj else None
        status = obj.get("status") if obj else None
        if status in ("superseded", "reversed", "abandoned"):
            continue
        if review:
            days = _days_until(review, now)
            if days is not None and days <= 0:
                recommendations.append({
                    "review_type": "decision-review",
                    "domain": "knowledge",
                    "object_id": item["object_id"],
                    "title": item.get("title"),
                    "priority": "critical" if days < -7 else "high",
                    "reason": f"decision review_date was {review}; overdue by {-days} day(s).",
                    "delegated_workflow": "workflows/core/review-decision.md",
                    "provenance": item.get("provenance"),
                })
            elif days is not None and days <= 14:
                recommendations.append({
                    "review_type": "decision-review",
                    "domain": "knowledge",
                    "object_id": item["object_id"],
                    "title": item.get("title"),
                    "priority": "normal" if days > 7 else "high",
                    "reason": f"decision review_date is in {days} day(s).",
                    "delegated_workflow": "workflows/core/review-decision.md",
                    "provenance": item.get("provenance"),
                })

    # 2. Goal reviews from priority mismatches.
    goal_mismatches = [f for f in findings if f["type"] == "priority_mismatch"]
    if not goal_mismatches:
        skipped.append({"review_type": "goal-review", "reason": "no active goal mismatches"})
    for f in goal_mismatches:
        for gid in f["object_ids"]:
            item = retriever.get_object(gid)
            if item and item.get("schema") == "planning.goal":
                recommendations.append({
                    "review_type": "goal-review",
                    "domain": "planning",
                    "object_id": gid,
                    "title": item.get("title"),
                    "priority": "high",
                    "reason": "active goal has little or no active supporting work.",
                    "delegated_workflow": "workflows/planning/review-goal.md",
                    "provenance": item.get("provenance"),
                })

    # 3. Learning reviews for approaching assessment or completion target.
    learning_programs = [
        item for item in bundle.get("current_state", []) + bundle.get("relevant_history", [])
        if item.get("object_schema") == "knowledge.learning-program"
    ]
    if not learning_programs:
        skipped.append({"review_type": "learning-review", "reason": "no active learning programs"})
    for item in learning_programs:
        obj = retriever.get_object(item["object_id"])
        target = _parse_date(obj.get("target_completion_date")) if obj else None
        assessment = _parse_date(obj.get("assessment_date")) if obj else None
        for d, label in ((target, "target completion"), (assessment, "assessment")):
            if d:
                days = _days_until(d, now)
                if days is not None and days <= 14:
                    recommendations.append({
                        "review_type": "learning-review",
                        "domain": "knowledge",
                        "object_id": item["object_id"],
                        "title": item.get("title"),
                        "priority": "high" if days <= 7 else "normal",
                        "reason": f"{label} is in {days} day(s).",
                        "delegated_workflow": "workflows/knowledge/guided-learning.md",
                        "provenance": item.get("provenance"),
                    })

    # 4. Knowledge retention reviews.
    # For now, surface if a knowledge.review object is present and due.
    reviews = [
        item for item in bundle.get("current_state", []) + bundle.get("relevant_history", [])
        if item.get("object_schema") == "knowledge.review"
    ]
    if not reviews:
        skipped.append({"review_type": "knowledge-retention", "reason": "no due review objects"})
    for item in reviews:
        obj = retriever.get_object(item["object_id"])
        due = _parse_date(obj.get("next_review_at")) if obj else None
        if due and due <= now:
            recommendations.append({
                "review_type": "knowledge-retention",
                "domain": "knowledge",
                "object_id": item["object_id"],
                "title": item.get("title"),
                "priority": "normal",
                "reason": f"retention review is due as of {due}.",
                "delegated_workflow": "workflows/core/review.md",
                "provenance": item.get("provenance"),
            })

    # 5. Domain-skipping: if a domain has no objects and no cross-domain findings, skip.
    domain_counts = {}
    for section in ("current_state", "relevant_history", "related_knowledge", "active_constraints"):
        for item in bundle.get(section, []):
            domain_counts[item.get("domain")] = domain_counts.get(item.get("domain"), 0) + 1
    for domain in ("finance", "health", "music"):
        if domain not in domain_counts or domain_counts[domain] == 0:
            skipped.append({"review_type": f"{domain}-review", "reason": "no relevant state in context"})

    # Deduplicate and sort by priority, then bound.
    priority_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}
    seen = set()
    unique = []
    for rec in recommendations:
        key = (rec["review_type"], rec["object_id"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(rec)

    unique.sort(key=lambda r: (priority_order.get(r["priority"], 4), r["reason"]))
    bounded = unique[:max_recommendations]

    return {
        "date": now.isoformat(),
        "recommendations": bounded,
        "skipped": skipped,
        "provenance": {
            "source": "scripts/core/review_orchestrator.py",
            "assembled_from": bundle.get("provenance", {}).get("retrieved_from", []),
            "reasoning_findings_count": len(findings),
        },
    }


if __name__ == "__main__":
    request = {
        "intent": "sunday-review",
        "query": "What should I review this week?",
        "domains": ["planning", "knowledge", "career"],
        "desired_depth": "deep",
        "avoid_domains": ["health", "finance", "music"],
    }
    bundle = assemble(request, demo_only=True)
    plan = orchestrate(bundle, current_date=date(2026, 8, 28))
    for rec in plan["recommendations"]:
        print(f"[{rec['priority']}] {rec['review_type']}: {rec['title']} ({rec['reason']})")
