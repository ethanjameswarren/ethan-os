#!/usr/bin/env python3
"""
Lightweight friction-log capture and review for Ethan OS.

Handles:
- creating or updating core.friction-log entries in ethan-life
- applying runtime context without asking unnecessary questions
- grouping, triage, and light reporting for review workflows
- converting repeated patterns into evaluation candidates

Actual personal entries are written to ethan-life; this module is public
and contains no private data by default.
"""

from __future__ import annotations

import re
import yaml
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

DEFAULT_STATUS = "open"
OPEN_STATUSES = {"open", "triaged", "planned"}
RESOLVED_STATUSES = {"fixed", "validated", "wont_fix", "cannot_reproduce"}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _today_iso() -> str:
    return _today().isoformat()


def _make_id(prefix: str = "friction") -> str:
    now = datetime.now(timezone.utc)
    return f"{prefix}-{_today().strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z0-9_-]+", text or "")]


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def load_friction_entries(root: Path) -> dict[str, dict]:
    """Load all core.friction-log objects from a directory tree."""
    entries = {}
    if not root.exists():
        return entries
    for path in sorted(root.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm or fm.get("schema") != "core.friction-log" or "id" not in fm:
            continue
        fm["_path"] = str(path)
        fm["_body"] = body
        entries[fm["id"]] = fm
    return entries


def infer_feedback_type(phrase: str) -> str:
    """Map a user phrase to a feedback_type category."""
    p = (phrase or "").lower()
    if "already know" in p or ("asked" in p and "knew" in p) or "should already" in p:
        return "asked_known_information"
    if "wrong context" in p or "pulled the wrong" in p:
        return "wrong_context"
    if "pulled" in p and "for no reason" in p:
        return "irrelevant_context"
    if "missed" in p and "connect" in p:
        return "missed_connection"
    if "too many questions" in p:
        return "excessive_questions"
    if "too long" in p and "review" in p:
        return "review_fatigue"
    if "too long" in p or ("too much" in p and "output" in p):
        return "excessive_output"
    if "saved too much" in p or "save too much" in p:
        return "saved_too_much"
    if "didn't save" in p or "failed to save" in p:
        return "failed_to_save"
    if "under explained" in p or "too short" in p:
        return "under_explained"
    if "over explained" in p or "too much detail" in p:
        return "over_explained"
    if "generic" in p or "bad recommendation" in p:
        return "bad_recommendation"
    if "workflow" in p and ("too long" in p or "should have called" in p):
        return "workflow_mismatch"
    if "stale" in p:
        return "stale_state"
    if "duplicate" in p:
        return "duplicate_state"
    if "didn't understand" in p or "awkward" in p:
        return "awkward_interaction"
    if "exactly right" in p or "felt natural" in p or "didn't ask me anything unnecessary" in p:
        return "worked_well"
    if "annoy" in p:
        return "other"
    return "other"


def infer_severity(feedback_type: str | None, phrase: str = "") -> str:
    """Infer severity from type and user phrasing."""
    phrase = (phrase or "").lower()
    if any(s in phrase for s in ("privacy", "corrupt", "deleted", "destructive", "serious")):
        return "critical"
    if feedback_type in {
        "wrong_context",
        "missed_orchestration",
        "bad_recommendation",
        "incorrect_reasoning",
        "stale_state",
        "wrong_persistence",
    }:
        return "high"
    if feedback_type in {
        "asked_known_information",
        "excessive_questions",
        "saved_too_much",
        "missed_connection",
        "failed_to_save",
    }:
        return "medium"
    if feedback_type == "worked_well":
        return "low"
    return "low"


def infer_root_cause(feedback_type: str | None) -> str:
    """Tentatively infer a root-cause area from the feedback type."""
    mapping = {
        "asked_known_information": "context_assembly",
        "irrelevant_context": "retrieval",
        "missing_context": "context_assembly",
        "wrong_context": "retrieval",
        "missed_connection": "reasoning",
        "excessive_questions": "confirmation",
        "excessive_output": "reasoning",
        "under_explained": "documentation",
        "over_explained": "reasoning",
        "saved_too_much": "persistence",
        "failed_to_save": "persistence",
        "wrong_persistence": "persistence",
        "workflow_mismatch": "workflow",
        "missed_orchestration": "orchestration",
        "bad_recommendation": "reasoning",
        "review_fatigue": "workflow",
        "awkward_interaction": "confirmation",
        "incorrect_reasoning": "reasoning",
        "stale_state": "persistence",
        "duplicate_state": "persistence",
        "unclear_confirmation": "confirmation",
    }
    return mapping.get(feedback_type, "unknown")


def apply_runtime_context(entry: dict, context: dict | None) -> dict:
    """Fill in workflow/capability/domain from runtime context if not already known."""
    if not context:
        return entry
    if not entry.get("affected_workflow") and context.get("current_workflow"):
        entry["affected_workflow"] = context["current_workflow"]
    if not entry.get("affected_skill") and context.get("current_skill"):
        entry["affected_skill"] = context["current_skill"]
    if not entry.get("affected_capability") and context.get("current_capability"):
        entry["affected_capability"] = context["current_capability"]
    if not entry.get("relevant_domain") and context.get("current_domain"):
        entry["relevant_domain"] = context["current_domain"]
    if not entry.get("context_bundle_id") and context.get("context_bundle_id"):
        entry["context_bundle_id"] = context["context_bundle_id"]
    if context.get("context_refs"):
        existing = set(entry.get("context_refs", []) or [])
        existing.update(context["context_refs"])
        entry["context_refs"] = sorted(existing)
    return entry


def find_similar_open(entries: dict[str, dict], candidate: dict) -> dict | None:
    """Return an open friction with the same type, capability, and workflow."""
    for e in entries.values():
        if e.get("status") not in OPEN_STATUSES:
            continue
        if (
            e.get("feedback_type") == candidate.get("feedback_type")
            and e.get("affected_capability") == candidate.get("affected_capability")
            and e.get("affected_workflow") == candidate.get("affected_workflow")
            and candidate.get("feedback_type")
            and candidate.get("affected_capability")
        ):
            return e
    return None


def prepare_friction_entry(
    user_phrase: str,
    summary: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
    context: dict | None = None,
    overrides: dict | None = None,
) -> dict:
    """Build a friction-log entry from a user statement and available runtime context."""
    feedback_type = (overrides or {}).get("feedback_type") or infer_feedback_type(user_phrase)
    is_positive = feedback_type == "worked_well"
    entry = {
        "schema": "core.friction-log",
        "schema_version": 1,
        "status": DEFAULT_STATUS,
        "summary": summary or user_phrase,
        "description": user_phrase if summary else None,
        "feedback_type": feedback_type,
        "user_expectation": expected,
        "observed_behavior": observed,
        "severity": (overrides or {}).get("severity") or infer_severity(feedback_type, user_phrase),
        "frequency": "once",
        "occurrence_count": 1,
        "occurrence_dates": [_today_iso()],
        "is_positive": is_positive,
        "source_phrase": user_phrase,
        "root_cause_inferred": (overrides or {}).get("root_cause_inferred")
                              or infer_root_cause(feedback_type),
        "root_cause_inference_note": (overrides or {}).get("root_cause_inference_note")
                                    or "Inferred from feedback type and runtime context. Not confirmed.",
        "provenance": {
            "agent_version": "ethan-os-0.1.0",
            "provenance_note": "Captured from user friction report.",
        },
    }
    if is_positive:
        entry["positive_outcome"] = summary or user_phrase
    if overrides:
        for key, value in overrides.items():
            if value is not None:
                entry[key] = value
    apply_runtime_context(entry, context)
    if not entry.get("title"):
        entry["title"] = (entry["summary"] or "").split(".")[0][:80]
    if not entry.get("id"):
        entry["id"] = _make_id()
    if not entry.get("created_at"):
        entry["created_at"] = _today_iso()
    if not entry.get("updated_at"):
        entry["updated_at"] = _today_iso()
    return entry


def write_friction_object(path: Path, obj: dict) -> Path:
    """Serialize a friction object to a Markdown file with YAML frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    internal = {"_path", "_body"}
    fm = {k: v for k, v in obj.items() if v is not None and k not in internal}
    body = obj.get("_body", "") or ""
    text = f"---\n{yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)}---\n\n{body}"
    path.write_text(text, encoding="utf-8")
    return path


def create_or_update_friction_entry(
    root: Path,
    entry: dict,
) -> tuple[dict, bool]:
    """Write a friction entry, updating an open duplicate if one exists."""
    entries = load_friction_entries(root)
    similar = find_similar_open(entries, entry)
    now = _today_iso()

    if similar:
        path = Path(similar["_path"])
        similar["updated_at"] = now
        similar["occurrence_count"] = similar.get("occurrence_count", 1) + 1
        similar["frequency"] = "repeated" if similar["occurrence_count"] >= 2 else "once"
        similar["occurrence_dates"] = similar.get("occurrence_dates", [similar.get("created_at")]) or []
        if now not in similar["occurrence_dates"]:
            similar["occurrence_dates"].append(now)
        for ref in entry.get("occurrence_context_refs", []) or []:
            existing = similar.setdefault("occurrence_context_refs", [])
            if ref not in existing:
                existing.append(ref)
        for ref in entry.get("context_refs", []) or []:
            existing = similar.setdefault("context_refs", [])
            if ref not in existing:
                existing.append(ref)
        write_friction_object(path, similar)
        return similar, False

    entry.setdefault("created_at", now)
    entry.setdefault("updated_at", now)
    path = root / f"{entry['id']}.md"
    write_friction_object(path, entry)
    return entry, True


def group_friction(entries: dict[str, dict]) -> dict:
    """Group friction entries by capability, type, root cause, severity, and repetition."""
    groups = {
        "by_capability": defaultdict(list),
        "by_feedback_type": defaultdict(list),
        "by_root_cause": defaultdict(list),
        "by_severity": defaultdict(list),
        "repeated": [],
        "positive": [],
    }
    for e in entries.values():
        groups["by_capability"][e.get("affected_capability", "Unknown")].append(e)
        groups["by_feedback_type"][e.get("feedback_type", "other")].append(e)
        groups["by_root_cause"][e.get("root_cause_inferred", "unknown")].append(e)
        groups["by_severity"][e.get("severity", "low")].append(e)
        if e.get("occurrence_count", 1) > 1 and not e.get("is_positive"):
            groups["repeated"].append(e)
        if e.get("is_positive"):
            groups["positive"].append(e)
    return {k: (dict(v) if isinstance(v, defaultdict) else v) for k, v in groups.items()}


def top_open_friction(
    entries: dict[str, dict],
    n: int = 7,
    include_positive: bool = False,
) -> list[dict]:
    """Return the most important open issues, by severity and repetition."""
    candidates = [e for e in entries.values() if e.get("status") in OPEN_STATUSES]
    if not include_positive:
        candidates = [e for e in candidates if not e.get("is_positive")]
    candidates.sort(
        key=lambda e: (
            SEVERITY_ORDER.get(e.get("severity", "low"), 4),
            -e.get("occurrence_count", 1),
            e.get("created_at", ""),
        )
    )
    return candidates[:n]


def suggest_evaluation_expectation(entry: dict) -> str | None:
    """Turn a friction pattern into a draft evaluation expectation."""
    if not entry:
        return None
    ft = entry.get("feedback_type")
    cap = entry.get("affected_capability", "the workflow")
    exp = entry.get("user_expectation", "")
    obs = entry.get("observed_behavior", "")
    if ft == "asked_known_information" and "active" in exp.lower():
        return f"If exactly one active {cap} state is already known, {cap} should not ask the user to identify it."
    if ft == "excessive_questions" and cap:
        return f"{cap} should ask no more than the minimum questions needed to proceed."
    if ft == "wrong_context" and cap:
        return f"{cap} should only pull context that is relevant to the current request."
    if ft == "missed_connection" and exp:
        return f"{cap} should connect the current request to the user's {exp}."
    if obs:
        return f"{cap} should not: {obs}"
    return f"{cap} should satisfy: {exp}" if exp else None
