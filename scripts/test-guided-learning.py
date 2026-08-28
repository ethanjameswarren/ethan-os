#!/usr/bin/env python3
"""
Guided Learning deterministic tests for Ethan OS.

Checks:
- learning-program objects are well-formed
- learning-session objects reference existing programs and valid modules
- course_type, status, desired_depth, prior_familiarity, and session_type are valid
- mistakes and insights have required fields
- program module references are consistent
"""

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "config" / "demo-personality" / "fixtures" / "domains" / "knowledge"
ETHAN_LIFE = ROOT.parent / "ethan-life"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def load_objects(folder: Path):
    objects = {}
    if not folder.exists():
        return objects
    for path in folder.rglob("*.md"):
        if path.name == "README.md":
            continue
        fm, _ = parse_frontmatter(path)
        if fm and "id" in fm:
            objects[fm["id"]] = fm
    return objects


VALID_COURSE_TYPES = {
    "university_course",
    "online_course",
    "certification",
    "workplace_training",
    "self_study",
    "other",
}

VALID_PROGRAM_STATUS = {
    "unread",
    "learning",
    "paused",
    "finished",
    "abandoned",
    "reference",
}

VALID_DEPTHS = {"light", "normal", "deep"}
VALID_FAMILIARITY = {"unfamiliar", "some_exposure", "familiar", "very_familiar"}

VALID_SESSION_TYPES = {
    "lecture",
    "video",
    "reading",
    "lab",
    "exercise",
    "homework",
    "assignment",
    "project",
    "study",
    "review",
    "quiz",
    "office_hours",
    "exam_prep",
    "other",
}

VALID_ASSESSMENT_TYPES = {
    "quiz",
    "midterm",
    "final",
    "certification_exam",
    "practical_exam",
    "project",
    "presentation",
    "course_completion",
    "other",
}


def validate_programs(programs: dict, label: str, broken: list):
    for pid, prog in programs.items():
        prefix = f"{label} program {pid}"

        ct = prog.get("course_type")
        if ct not in VALID_COURSE_TYPES:
            broken.append(f"{prefix}: invalid course_type '{ct}'")

        status = prog.get("status")
        if status and status not in VALID_PROGRAM_STATUS:
            broken.append(f"{prefix}: invalid status '{status}'")

        depth = prog.get("desired_depth")
        if depth and depth not in VALID_DEPTHS:
            broken.append(f"{prefix}: invalid desired_depth '{depth}'")

        fam = prog.get("prior_familiarity")
        if fam and fam not in VALID_FAMILIARITY:
            broken.append(f"{prefix}: invalid prior_familiarity '{fam}'")

        modules = prog.get("modules") or []
        module_ids = {m.get("id") for m in modules if m.get("id")}

        current = prog.get("current_module_id")
        if current and current not in module_ids:
            broken.append(f"{prefix}: current_module_id '{current}' not found in modules")

        for completed in prog.get("completed_module_ids", []):
            if completed not in module_ids:
                broken.append(f"{prefix}: completed_module_id '{completed}' not found in modules")

        for assessment in prog.get("assessments", []):
            atype = assessment.get("type")
            if atype not in VALID_ASSESSMENT_TYPES:
                broken.append(f"{prefix}: invalid assessment type '{atype}'")



def validate_sessions(sessions: dict, programs: dict, label: str, broken: list):
    for sid, session in sessions.items():
        prefix = f"{label} session {sid}"

        st = session.get("session_type")
        if st not in VALID_SESSION_TYPES:
            broken.append(f"{prefix}: invalid session_type '{st}'")

        program_id = session.get("program_id")
        if not program_id:
            broken.append(f"{prefix}: missing program_id")
            continue
        if program_id not in programs:
            broken.append(f"{prefix}: program_id '{program_id}' not found")
            continue

        program = programs[program_id]
        module_ids = {m.get("id") for m in program.get("modules", []) if m.get("id")}
        module_id = session.get("module_id")
        if module_id and module_id not in module_ids:
            broken.append(f"{prefix}: module_id '{module_id}' not found in program '{program_id}'")

        for insight in session.get("extracted_insights", []):
            if not insight.get("insight_id") or not insight.get("title"):
                broken.append(f"{prefix}: extracted_insight missing insight_id or title")

        for mistake in session.get("mistakes", []):
            if not mistake.get("description"):
                broken.append(f"{prefix}: mistake missing description")


def main():
    print("Guided Learning deterministic tests")
    print("=" * 40)

    broken = []

    demo_programs = load_objects(FIXTURES / "learning-programs")
    demo_sessions = load_objects(FIXTURES / "learning-sessions")
    life_programs = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "learning-programs")
    life_sessions = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "learning-sessions")

    validate_programs(demo_programs, "demo", broken)
    validate_sessions(demo_sessions, demo_programs, "demo", broken)
    validate_programs(life_programs, "ethan-life", broken)
    validate_sessions(life_sessions, life_programs, "ethan-life", broken)

    print(f"Checked {len(demo_programs) + len(life_programs)} programs, "
          f"{len(demo_sessions) + len(life_sessions)} sessions")

    if broken:
        print(f"\nFAILURES ({len(broken)}):")
        for item in broken:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("\nAll Guided Learning checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
