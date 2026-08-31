#!/usr/bin/env python3
"""
Context Assembly for Ethan OS.

Given a context request, use universal retrieval to produce a bounded,
privacy-respecting, provenance-backed context bundle.
"""

from datetime import datetime, timezone
from pathlib import Path

from universal_retrieval import UniversalRetriever, _is_active


LIGHT_LIMIT = 5
NORMAL_LIMIT = 15
DEEP_LIMIT = 30


def _depth_to_k(desired_depth: str) -> int:
    return {"light": LIGHT_LIMIT, "normal": NORMAL_LIMIT}.get(desired_depth, DEEP_LIMIT)


def _depth_to_retrieval_depth(desired_depth: str) -> str:
    return "direct" if desired_depth == "light" else ("deep" if desired_depth == "deep" else "direct")


def _now_utc():
    return datetime.now(timezone.utc)


def assemble(request: dict, retriever: UniversalRetriever | None = None, demo_only: bool = False, life_root: Path | None = None) -> dict:
    """Assemble a context bundle from a context request."""
    if retriever is None:
        from universal_retrieval import build_retriever
        retriever = build_retriever(demo_only=demo_only, life_root=life_root)

    intent = request.get("intent", "")
    query = request.get("query", request.get("user_input", ""))
    domains = request.get("domains")
    avoid = request.get("avoid_domains", [])
    entity_refs = request.get("entity_refs", [])
    desired_depth = request.get("desired_depth", "normal")
    time_horizon = request.get("time_horizon", "now")

    top_k = _depth_to_k(desired_depth)
    depth = _depth_to_retrieval_depth(desired_depth)

    # Light is more selective: prefer active and exact references.
    statuses = None
    if desired_depth == "light":
        statuses = ["active", "reading", "learning", "in_progress", "accepted", "current"]

    retrieval = retriever.retrieve(
        query=query,
        intent=intent,
        domains=domains,
        avoid_domains=avoid,
        entity_refs=entity_refs,
        top_k=top_k,
        depth=depth,
        time_horizon=time_horizon,
        statuses=statuses,
    )
    results = retrieval["results"]
    unresolved_refs = retrieval["unresolved_refs"]

    # Build a map of object details.
    object_map = {}
    for r in results:
        obj = retriever.get_object(r["object_id"])
        if obj:
            object_map[r["object_id"]] = obj

    # Split into bundle categories.
    current_state = []
    relevant_history = []
    related_knowledge = []
    active_constraints = []

    for r in results:
        obj = object_map.get(r["object_id"])
        if not obj:
            continue

        category = _category_for(obj, r["domain"])
        entry = {
            "domain": r["domain"],
            "object_id": r["object_id"],
            "object_schema": r["schema"],
            "title": r["title"],
            "status": r["status"],
            "summary": _summarize(obj, desired_depth),
            "relevance_explanation": r["relevance_explanation"],
            "source_path": r["source_path"],
            "provenance": r["provenance"],
        }

        if category == "knowledge":
            related_knowledge.append(entry)
        elif category == "constraint":
            active_constraints.append({
                "constraint_type": _constraint_type(obj),
                "description": entry["summary"],
                "object_id": entry["object_id"],
                "provenance": entry["provenance"],
            })
        elif _is_active(obj) or _is_current(obj):
            current_state.append(entry)
        else:
            relevant_history.append({
                "object_id": entry["object_id"],
                "summary": entry["summary"],
                "relevance_reason": r["relevance_explanation"],
            })

    # Preferences from global design-philosophy if available.
    preferences = []
    design_philosophy = _load_global_design_philosophy(retriever)
    if design_philosophy:
        preferences.append({
            "preference_type": "design_philosophy",
            "description": design_philosophy[:200] + ("..." if len(design_philosophy) > 200 else ""),
        })

    bundle = {
        "request": request,
        "current_state": current_state,
        "relevant_history": relevant_history,
        "related_knowledge": related_knowledge,
        "active_constraints": active_constraints,
        "preferences": preferences,
        "unresolved_refs": unresolved_refs,
        "provenance": {
            "source": "skills/core/context-assembly",
            "retrieved_from": ["ethan-life/domains", "ethan-os/config/demo-personality/fixtures/domains"],
            "assembled_at": _now_utc().isoformat(),
        },
        "assembled_at": _now_utc().isoformat(),
    }

    return bundle


def _category_for(obj: dict, domain: str) -> str:
    schema = obj.get("schema", "")
    if domain == "knowledge" and schema in ("knowledge.idea", "knowledge.summary"):
        return "knowledge"
    if domain == "planning" and schema in ("planning.baseline-schedule", "planning.schedule-override"):
        return "constraint"
    if "schedule" in schema or "override" in schema:
        return "constraint"
    return "state"


def _constraint_type(obj: dict) -> str:
    schema = obj.get("schema", "")
    if "baseline-schedule" in schema:
        return "schedule"
    if "schedule-override" in schema:
        return "schedule"
    if "goal" in schema:
        return "goal"
    if "task" in schema:
        return "deadline"
    return "preference"


def _is_current(obj: dict) -> bool:
    return _is_active(obj)


def _summarize(obj: dict, depth: str) -> str:
    title = obj.get("title", "")
    if depth == "light":
        return title
    if depth == "deep":
        parts = [title]
        for key in ("description", "why_it_matters", "claim", "interpretation"):
            if obj.get(key):
                parts.append(str(obj.get(key)))
        return "; ".join(parts)
    return f"{title}: {obj.get('description', obj.get('why_it_matters', ''))}".strip(": ")


def _load_global_design_philosophy(retriever: UniversalRetriever) -> str:
    # Look for a global design-philosophy object in fixtures or ethan-life/global.
    for root in retriever.roots:
        if not root:
            continue
        for path in Path(root).rglob("*.md"):
            if path.stem == "design-philosophy":
                _, body = _parse_frontmatter(path)
                return body.strip()
    return ""


def _parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    import re
    FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return None, text


if __name__ == "__main__":
    import json
    request = {
        "intent": "course-decision",
        "query": "Should I take this LinkedIn Learning agentic AI course?",
        "domains": ["planning", "knowledge", "career"],
        "avoid_domains": ["health", "finance", "music"],
        "desired_depth": "normal",
        "time_horizon": "now",
    }
    bundle = assemble(request)
    print(json.dumps(bundle, indent=2, default=str))
