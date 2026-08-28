#!/usr/bin/env python3
"""
Capability validation matrix helper for Ethan OS.

Reads the private validation matrix from ethan-life and provides
queries that support the "Validate and Harden Ethan OS" goal.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_MATRIX = ROOT.parent / "ethan-life" / "domains" / "system" / "validation-matrix.yaml"


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def load_matrix(path: Path | None = None) -> dict:
    p = path or DEFAULT_MATRIX
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_matrix(matrix: dict, path: Path | None = None) -> None:
    p = path or DEFAULT_MATRIX
    p.parent.mkdir(parents=True, exist_ok=True)
    matrix["updated_at"] = _today()
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(matrix, f, sort_keys=False, allow_unicode=True)


def capability_by_name(matrix: dict, name: str) -> dict | None:
    for c in matrix.get("capabilities", []):
        if c.get("capability") == name:
            return c
    return None


def record_use(
    matrix: dict,
    capability_name: str,
    workflow: str,
    scenario: str,
    outcome: str = "success",
    friction_refs: list[str] | None = None,
    mark_happy: bool = False,
    mark_edge: bool = False,
    mark_failure: bool = False,
    mark_cross_domain: bool = False,
    mark_persistence: bool = False,
) -> dict | None:
    """Record a real-world use of a capability, distinguishing outcome and coverage."""
    cap = capability_by_name(matrix, capability_name)
    if cap is None:
        return None

    cap["real_world_uses"] = cap.get("real_world_uses", 0) + 1
    if outcome == "success":
        cap["successful_uses"] = cap.get("successful_uses", 0) + 1
    elif outcome == "partial":
        cap["partial_uses"] = cap.get("partial_uses", 0) + 1
    elif outcome in ("failed", "friction"):
        cap["failed_uses"] = cap.get("failed_uses", 0) + 1
    if outcome == "friction":
        cap["friction_observations"] = cap.get("friction_observations", 0) + 1

    cap["last_tested"] = _today()
    coverage = set(cap.get("scenario_coverage", []))
    coverage.add(scenario)
    cap["scenario_coverage"] = sorted(coverage)
    cap["coverage_breadth"] = len(cap["scenario_coverage"])

    if mark_happy:
        cap["happy_path"] = True
    if mark_edge:
        cap["edge_cases"] = True
    if mark_failure:
        cap["failure_recovery"] = True
    if mark_cross_domain:
        cap["cross_domain"] = True
    if mark_persistence:
        cap["persistence_validated"] = True
    if friction_refs:
        existing = set(cap.get("evidence_refs", []))
        existing.update(friction_refs)
        cap["evidence_refs"] = sorted(existing)
    return cap


def least_tested(matrix: dict, n: int = 5, min_level: int = 0) -> list[dict]:
    """Return the capabilities with the lowest validation evidence."""
    caps = [c for c in matrix.get("capabilities", []) if c.get("validation_level", 0) <= min_level]
    caps.sort(
        key=lambda c: (
            c.get("validation_level", 0),
            c.get("real_world_uses", 0),
            c.get("unresolved_issues", 0),
            c.get("last_tested") or "9999-12-31",
        )
    )
    return caps[:n]


def next_validation(matrix: dict, n: int = 3) -> list[dict]:
    """Return capabilities with explicit next-validation guidance."""
    caps = [c for c in matrix.get("capabilities", []) if c.get("next_validation")]
    caps.sort(
        key=lambda c: (
            c.get("validation_level", 0),
            c.get("real_world_uses", 0),
        )
    )
    return caps[:n]


def summary(matrix: dict) -> dict:
    caps = matrix.get("capabilities", [])
    return {
        "total": len(caps),
        "untested": len([c for c in caps if c.get("validation_level", 0) == 0]),
        "smoke_tested": len([c for c in caps if c.get("validation_level", 0) >= 1]),
        "scenario_validated": len([c for c in caps if c.get("validation_level", 0) >= 3]),
        "repeatedly_proven": len([c for c in caps if c.get("validation_level", 0) >= 5]),
        "successful_uses": sum(c.get("successful_uses", 0) for c in caps),
        "partial_uses": sum(c.get("partial_uses", 0) for c in caps),
        "failed_uses": sum(c.get("failed_uses", 0) for c in caps),
        "with_open_friction": len([c for c in caps if c.get("friction_observations", 0) > 0]),
    }


def main():
    parser = argparse.ArgumentParser(description="Ethan OS validation matrix helper")
    parser.add_argument("--matrix", type=Path, help="Path to validation-matrix.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    ls = sub.add_parser("least-tested", help="Show least-tested capabilities")
    ls.add_argument("--n", type=int, default=5)
    ls.add_argument("--max-level", type=int, default=0, dest="min_level")

    rec = sub.add_parser("record-use", help="Record a real-world use")
    rec.add_argument("capability")
    rec.add_argument("workflow")
    rec.add_argument("scenario")
    rec.add_argument("--outcome", choices=["success", "partial", "failed", "friction"], default="success")
    rec.add_argument("--friction-refs", nargs="*")
    rec.add_argument("--happy", action="store_true")
    rec.add_argument("--edge", action="store_true")
    rec.add_argument("--failure", action="store_true")
    rec.add_argument("--cross-domain", action="store_true")
    rec.add_argument("--persistence", action="store_true")

    sum_p = sub.add_parser("summary", help="Show matrix summary")
    next_p = sub.add_parser("next", help="Show next-validation candidates")
    next_p.add_argument("--n", type=int, default=3)

    args = parser.parse_args()
    matrix = load_matrix(args.matrix)
    levels = matrix.get("validation_levels", {})

    if args.command == "least-tested":
        for c in least_tested(matrix, n=args.n, min_level=args.min_level):
            lvl = c.get("validation_level", 0)
            print(f"- {c['capability']}: level {lvl} ({levels.get(lvl, '?')}), total {c.get('real_world_uses', 0)}, success {c.get('successful_uses', 0)}, failed {c.get('failed_uses', 0)}, coverage {c.get('coverage_breadth', 0)}, last tested {c.get('last_tested') or 'never'}")

    elif args.command == "record-use":
        cap = record_use(
            matrix,
            args.capability,
            args.workflow,
            args.scenario,
            outcome=args.outcome,
            friction_refs=args.friction_refs,
            mark_happy=args.happy,
            mark_edge=args.edge,
            mark_failure=args.failure,
            mark_cross_domain=args.cross_domain,
            mark_persistence=args.persistence,
        )
        if cap is None:
            print(f"Capability not found: {args.capability}")
            raise SystemExit(1)
        save_matrix(matrix, args.matrix)
        print(f"Recorded use of {args.capability} for {args.workflow} ({args.scenario}).")

    elif args.command == "summary":
        s = summary(matrix)
        for k, v in s.items():
            print(f"{k}: {v}")

    elif args.command == "next":
        for c in next_validation(matrix, n=args.n):
            print(f"- {c['capability']}: {c.get('next_validation')}")


if __name__ == "__main__":
    main()
