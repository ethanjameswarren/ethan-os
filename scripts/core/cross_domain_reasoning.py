#!/usr/bin/env python3
"""
Cross-Domain Reasoning for Ethan OS.

Reasons over an already assembled context bundle to identify:
- connections
- overlaps
- gaps
- conflicts
- dependencies
- transfer opportunities
- priority mismatches
- unsupported assumptions
- possible next actions

It does not retrieve new objects and does not perform domain-specific action.
"""

from pathlib import Path

from universal_retrieval import UniversalRetriever, build_retriever


DEFAULT_LIMIT = 7
SUPPORT_RELATIONS = {"supports", "applies_to", "part_of", "sourced_from", "tested_by"}
OPPOSITION_RELATIONS = {"contradicts", "conflicts_with"}


def _load_full_objects(bundle: dict, retriever: UniversalRetriever) -> dict[str, dict]:
    """Load full object records for all object IDs in the bundle."""
    ids = set()
    for section in ("current_state", "relevant_history", "related_knowledge", "active_constraints"):
        for item in bundle.get(section, []):
            ids.add(item.get("object_id"))

    objects = {}
    for obj_id in ids:
        obj = retriever.get_object(obj_id) if retriever else None
        if obj:
            objects[obj_id] = obj
    return objects


def _links_for(obj: dict) -> list[dict]:
    return obj.get("links", []) or []


def _title(objects: dict, obj_id: str) -> str:
    if obj_id in objects:
        return objects[obj_id].get("title") or obj_id
    return obj_id


def _schema(objects: dict, obj_id: str) -> str:
    if obj_id in objects:
        return objects[obj_id].get("schema", "")
    return ""


def _domain(schema: str) -> str:
    return schema.split(".")[0] if "." in schema else ""


def _tags_for(objects: dict, obj_id: str) -> set[str]:
    tags = objects.get(obj_id, {}).get("tags", []) or []
    return set(str(t).lower() for t in tags)


def _focal_obj(focal_id: str | None, objects: dict) -> dict | None:
    if not focal_id:
        return None
    return objects.get(focal_id)


def _is_active_status(status: str | None) -> bool:
    if not status:
        return False
    return status in {
        "active", "reading", "learning", "in_progress", "accepted",
        "current", "understood", "captured", "connected", "testing",
        "practicing", "internalized",
    }


def _object_type(schema: str) -> str:
    return schema.split(".")[-1] if "." in schema else schema


def reason(
    bundle: dict,
    retriever: UniversalRetriever | None = None,
    focal_id: str | None = None,
    modes: list[str] | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict]:
    """Produce cross-domain findings from a context bundle."""
    if retriever is None:
        retriever = build_retriever(demo_only=True)

    objects = _load_full_objects(bundle, retriever)
    modes = set(modes or [])
    all_modes = not modes
    findings = []

    # Pre-compute useful object lists across the bundle.
    goals = [oid for oid, o in objects.items() if o.get("schema", "") == "planning.goal"]
    projects = [oid for oid, o in objects.items() if o.get("schema", "") == "planning.project"]
    job_targets = [oid for oid, o in objects.items() if o.get("schema", "") == "career.job-target"]
    learning_sources = [oid for oid, o in objects.items() if o.get("schema", "") in ("knowledge.learning-program", "knowledge.source")]
    active_learning = [oid for oid in learning_sources if _is_active_status(objects[oid].get("status"))]
    active_goals = [oid for oid in goals if _is_active_status(objects[oid].get("status"))]

    # A. Explicit typed relationships in the bundle.
    if all_modes or "connection" in modes:
        for obj_id, obj in objects.items():
            for link in _links_for(obj):
                target = link.get("target")
                relation = link.get("relation", "related_to")
                if target not in objects:
                    continue
                target_obj = objects[target]
                statement = (
                    f"{_title(objects, obj_id)} ({_object_type(obj.get('schema',''))}) "
                    f"{relation} {_title(objects, target)} ({_object_type(target_obj.get('schema',''))})."
                )
                findings.append({
                    "type": _finding_type_for_relation(relation),
                    "statement": statement,
                    "object_ids": [obj_id, target],
                    "domains": sorted({_domain(obj.get("schema", "")), _domain(target_obj.get("schema", ""))}),
                    "evidence": {
                        "relation": relation,
                        "source_object": obj_id,
                        "target_object": target,
                        "note": link.get("note", ""),
                    },
                    "confidence": "high",
                    "why_it_matters": "Explicit typed links are the strongest form of cross-domain connection.",
                })

    # B. Transfer opportunities: learning/source can apply to project; project can become career evidence.
    if all_modes or "transfer_opportunity" in modes:
        learning = [oid for oid, o in objects.items() if o.get("schema", "").startswith("knowledge.")]
        projects = [oid for oid, o in objects.items() if o.get("schema", "") == "planning.project"]
        evidence = [oid for oid, o in objects.items() if o.get("schema", "") == "career.evidence"]

        for lp in learning:
            for proj in projects:
                if _share_concept(objects, lp, proj):
                    findings.append({
                        "type": "transfer_opportunity",
                        "statement": f"{_title(objects, lp)} could be applied to {_title(objects, proj)}.",
                        "object_ids": [lp, proj],
                        "domains": ["knowledge", "planning"],
                        "evidence": {
                            "shared_concepts": sorted(_shared_concepts(objects, lp, proj)),
                        },
                        "confidence": "medium",
                        "why_it_matters": "Applying learning to a project reinforces retention and creates practical evidence.",
                        "implication": "Use the project as the practical exercise for the course or source.",
                        "suggested_action": "Capture a learning session that explicitly uses the project as the context.",
                    })

        for proj in projects:
            for ev in evidence:
                if _share_concept(objects, proj, ev):
                    findings.append({
                        "type": "transfer_opportunity",
                        "statement": f"{_title(objects, proj)} could become {_title(objects, ev)} or strengthen it.",
                        "object_ids": [proj, ev],
                        "domains": ["planning", "career"],
                        "evidence": {
                            "shared_concepts": sorted(_shared_concepts(objects, proj, ev)),
                        },
                        "confidence": "medium",
                        "why_it_matters": "Projects are common sources of career evidence.",
                        "implication": "Frame the project as evidence when preparing for a relevant role.",
                    })

    # C. Gap detection.
    if all_modes or "gap" in modes:
        for goal in goals:
            if _is_active_status(objects.get(goal, {}).get("status")):
                linked = _linked_object_ids(objects, goal)
                has_project = any(objects.get(l, {}).get("schema", "") == "planning.project" for l in linked)
                has_learning = any(objects.get(l, {}).get("schema", "").startswith("knowledge.") for l in linked)
                has_evidence = any(objects.get(l, {}).get("schema", "") == "career.evidence" for l in linked)
                if not has_project:
                    findings.append({
                        "type": "evidence_gap",
                        "statement": f"{_title(objects, goal)} has no linked practical project.",
                        "object_ids": [goal],
                        "domains": ["planning"],
                        "evidence": {"linked_objects": linked},
                        "confidence": "medium",
                        "why_it_matters": "A goal with learning but no project may lack applied evidence.",
                        "suggested_action": "Create or link a project to the goal.",
                    })
                if not has_evidence and objects.get(goal, {}).get("horizon") == "medium_term":
                    findings.append({
                        "type": "evidence_gap",
                        "statement": f"{_title(objects, goal)} does not yet link to career evidence.",
                        "object_ids": [goal],
                        "domains": ["planning", "career"],
                        "evidence": {"linked_objects": linked},
                        "confidence": "low",
                        "why_it_matters": "For career-shifting goals, evidence of capability matters.",
                    })

        job_targets = [oid for oid, o in objects.items() if o.get("schema", "") == "career.job-target"]
        for jt in job_targets:
            linked = _linked_object_ids(objects, jt)
            has_evidence = any(objects.get(l, {}).get("schema", "") == "career.evidence" for l in linked)
            if not has_evidence:
                findings.append({
                    "type": "evidence_gap",
                    "statement": f"{_title(objects, jt)} has no directly linked career evidence.",
                    "object_ids": [jt],
                    "domains": ["career"],
                    "evidence": {"linked_objects": linked},
                    "confidence": "medium",
                    "why_it_matters": "A job target needs evidence to support applications.",
                    "suggested_action": "Identify a project or accomplishment that supports this target.",
                })

        projects = [oid for oid, o in objects.items() if o.get("schema", "") == "planning.project"]
        for proj in projects:
            linked = _linked_object_ids(objects, proj)
            has_task = any(objects.get(l, {}).get("schema", "") == "planning.task" for l in linked)
            if not has_task:
                findings.append({
                    "type": "gap",
                    "statement": f"{_title(objects, proj)} has no linked tasks.",
                    "object_ids": [proj],
                    "domains": ["planning"],
                    "evidence": {"linked_objects": linked},
                    "confidence": "medium",
                    "why_it_matters": "A project without tasks may not have execution defined.",
                    "suggested_action": "Add a first task to the project.",
                })

    # D. Overlap / duplication.
    if all_modes or "overlap" in modes:
        learning_sources = [oid for oid, o in objects.items() if o.get("schema", "") in ("knowledge.learning-program", "knowledge.source")]
        for i in range(len(learning_sources)):
            for j in range(i + 1, len(learning_sources)):
                a, b = learning_sources[i], learning_sources[j]
                shared = _shared_concepts(objects, a, b)
                if shared:
                    findings.append({
                        "type": "overlap",
                        "statement": f"{_title(objects, a)} and {_title(objects, b)} cover overlapping concepts.",
                        "object_ids": [a, b],
                        "domains": ["knowledge"],
                        "evidence": {"shared_concepts": sorted(shared)},
                        "confidence": "medium",
                        "why_it_matters": "The user may be spending time on similar material.",
                        "implication": "Consider whether the new one adds distinct depth.",
                    })

    # E. Priority mismatch: active goal/project with no execution.
    if all_modes or "priority_mismatch" in modes:
        for goal in goals:
            if _is_active_status(objects.get(goal, {}).get("status")):
                linked = _linked_object_ids(objects, goal)
                has_active_action = any(
                    _is_active_status(objects.get(l, {}).get("status"))
                    for l in linked
                    if objects.get(l, {}).get("schema", "") in ("planning.project", "planning.task", "knowledge.learning-program")
                )
                if not has_active_action:
                    findings.append({
                        "type": "priority_mismatch",
                        "statement": f"{_title(objects, goal)} is active but has no active linked project, task, or learning program.",
                        "object_ids": [goal],
                        "domains": ["planning"],
                        "evidence": {"linked_objects": linked},
                        "confidence": "medium",
                        "why_it_matters": "Stated priorities should connect to active execution.",
                        "suggested_action": "Decide whether to start supporting work or pause the goal.",
                    })

    # F. Conflict / tradeoff.
    if all_modes or "conflict" in modes or "tradeoff" in modes:
        # active_goals and active_learning were pre-computed.
        # Simple schedule heuristic: if multiple active learning programs and baseline schedule exists, flag.
        baseline = next((item for item in bundle.get("active_constraints", []) if item.get("constraint_type") == "schedule"), None)
        if baseline and len(active_learning) >= 2:
            findings.append({
                "type": "tradeoff",
                "statement": f"{len(active_learning)} active learning programs may compete for schedule time.",
                "object_ids": active_learning,
                "domains": ["knowledge", "planning"],
                "evidence": {"active_learning_count": len(active_learning), "schedule_constraint": baseline.get("object_id")},
                "confidence": "low",
                "why_it_matters": "Schedule capacity is finite. Multiple parallel learning commitments may not fit.",
                "suggested_action": "Compare target dates and decide whether to sequence or drop one.",
            })
        if len(active_goals) >= 2:
            findings.append({
                "type": "tradeoff",
                "statement": f"{len(active_goals)} active goals may compete for time and attention.",
                "object_ids": active_goals,
                "domains": ["planning"],
                "evidence": {"active_goal_count": len(active_goals)},
                "confidence": "low",
                "why_it_matters": "Too many active goals dilutes execution.",
                "suggested_action": "Identify the highest-priority one to three goals for this period.",
            })

    # G. Why trace / what supports focal.
    if focal_id:
        focal = _focal_obj(focal_id, objects)
        if focal:
            if _object_type(focal.get("schema", "")) == "goal":
                _what_supports_goal(focal_id, objects, findings)
            _why_trace(focal_id, objects, findings)

    # H. Orphan detection: active objects with no cross-domain links.
    if all_modes or "orphan" in modes:
        for obj_id, obj in objects.items():
            if not _is_active_status(obj.get("status")):
                continue
            schema = obj.get("schema", "")
            if schema == "planning.project" and not _linked_object_ids(objects, obj_id):
                findings.append({
                    "type": "stale_assumption",
                    "statement": f"{_title(objects, obj_id)} is active but not connected to a goal or other object.",
                    "object_ids": [obj_id],
                    "domains": ["planning"],
                    "evidence": {"linked_count": 0},
                    "confidence": "low",
                    "why_it_matters": "Projects without context may lack clear purpose or priority.",
                    "suggested_action": "Link this project to a goal or convert it to a capture.",
                })

    # Deduplicate and bound.
    seen = set()
    unique = []
    for f in findings:
        key = (f["type"], tuple(sorted(f["object_ids"])), f["statement"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)

    # Sort by confidence, then by number of domains involved, then statement.
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    unique.sort(key=lambda f: (confidence_order.get(f["confidence"], 3), -len(f.get("domains", [])), f["statement"]))

    return unique[:limit]


def _finding_type_for_relation(relation: str) -> str:
    if relation in SUPPORT_RELATIONS:
        return "connection"
    if relation in OPPOSITION_RELATIONS:
        return "conflict"
    return "connection"


def _linked_object_ids(objects: dict, obj_id: str) -> set[str]:
    obj = objects.get(obj_id, {})
    return {link.get("target") for link in _links_for(obj) if link.get("target")}


def _share_concept(objects: dict, a: str, b: str) -> bool:
    return bool(_shared_concepts(objects, a, b))


def _shared_concepts(objects: dict, a: str, b: str) -> set[str]:
    tags_a = _tags_for(objects, a)
    tags_b = _tags_for(objects, b)
    text_a = set(_words_in_object(objects, a))
    text_b = set(_words_in_object(objects, b))
    shared = (tags_a & tags_b) | (text_a & text_b)
    # Filter out very short words.
    return {s for s in shared if len(s) > 3}


def _flatten_values(value) -> list[str]:
    out = []
    if isinstance(value, dict):
        for k, v in value.items():
            if k in ("_path", "_domain"):
                continue
            out.extend(_flatten_values(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(_flatten_values(v))
    elif value is not None:
        out.append(str(value))
    return out


def _words_in_object(objects: dict, obj_id: str) -> list[str]:
    obj = objects.get(obj_id, {})
    pieces = [str(v) for k, v in obj.items() if k not in ("_path", "_domain")]
    pieces.extend(_flatten_values(obj))
    text = " ".join(pieces).lower()
    import re
    return re.findall(r"[a-z0-9_-]{4,}", text)


def _what_supports_goal(goal_id: str, objects: dict, findings: list[dict]):
    linked = _linked_object_ids(objects, goal_id)
    direct_support = []
    for l in linked:
        obj = objects.get(l, {})
        schema = obj.get("schema", "")
        if _is_active_status(obj.get("status")):
            direct_support.append({
                "object_id": l,
                "title": _title(objects, l),
                "type": _object_type(schema),
                "domain": _domain(schema),
            })
    if direct_support:
        findings.append({
            "type": "connection",
            "statement": f"{_title(objects, goal_id)} is currently supported by {len(direct_support)} active object(s).",
            "object_ids": [goal_id] + [d["object_id"] for d in direct_support],
            "domains": sorted({d["domain"] for d in direct_support if d["domain"]} | {"planning"}),
            "evidence": {"supporting_objects": direct_support},
            "confidence": "high",
            "why_it_matters": "Shows where active effort is already aligned with the goal.",
        })


def _why_trace(focal_id: str, objects: dict, findings: list[dict]):
    # Walk from focal toward goals.
    visited = {focal_id}
    frontier = [focal_id]
    path = [focal_id]
    while frontier:
        current = frontier.pop()
        obj = objects.get(current, {})
        for link in _links_for(obj):
            target = link.get("target")
            rel = link.get("relation", "")
            if target in visited:
                continue
            if rel in SUPPORT_RELATIONS or rel == "part_of" or rel == "sourced_from":
                visited.add(target)
                frontier.append(target)
                path.append(target)
                target_schema = _object_type(objects.get(target, {}).get("schema", ""))
                if target_schema == "goal" or objects.get(target, {}).get("schema", "").endswith("goal"):
                    chain = [_title(objects, p) for p in path]
                    findings.append({
                        "type": "connection",
                        "statement": f"{_title(objects, focal_id)} connects to {_title(objects, target)}: {' → '.join(chain)}.",
                        "object_ids": path,
                        "domains": sorted({_domain(objects.get(p, {}).get("schema", "")) for p in path}),
                        "evidence": {"path": path},
                        "confidence": "high",
                        "why_it_matters": "This explains why the focal object matters in the broader system.",
                    })
                    return


if __name__ == "__main__":
    from context_assembly import assemble
    request = {
        "intent": "course-decision",
        "query": "Should I take this LinkedIn Learning agentic AI course?",
        "domains": ["planning", "knowledge", "career"],
        "desired_depth": "deep",
    }
    bundle = assemble(request, demo_only=True)
    findings = reason(bundle, focal_id="goal-ai-engineering", limit=15)
    for f in findings:
        print(f"[{f['confidence']}] {f['type']}: {f['statement']}")
