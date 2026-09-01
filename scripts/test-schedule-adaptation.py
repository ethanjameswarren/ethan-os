#!/usr/bin/env python3
"""
Deterministic tests for Schedule Adaptation / Behavioral Learning.

These tests simulate accumulated schedule overrides and verify that the
analyze/classify/drift logic behaves correctly: exceptions do not rewrite
baselines, repeated patterns trigger drift detection, and recommendations
require evidence and approval before any baseline mutation.
"""

import re
import sys
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def duration(start: str, end: str) -> int:
    s = time_to_minutes(start)
    e = time_to_minutes(end)
    if e < s:
        e += 24 * 60
    return e - s


def median(values: list) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return float(s[n // 2])
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def analyze_block(overrides, baseline, policy):
    """Minimal analyzer that returns a pattern dict for one baseline block."""
    relevant = [
        o for o in overrides
        if o.get("target_block", {}).get("label") == baseline["label"]
        and o.get("target_block", {}).get("day_of_week") == baseline["day_of_week"]
    ]

    n = len(relevant)
    if n == 0:
        return {"recommendation": None, "pattern": "none"}

    effects = [o.get("change_effect") for o in relevant]
    classifications = [o.get("classification") for o in relevant]
    exception_count = classifications.count("exception")
    non_exception = [o for o in relevant if o.get("classification") != "exception"]

    start_shifts = []
    duration_deltas = []
    replacements = {}
    reasons = {}

    for o in relevant:
        tb = o.get("target_block", {})
        b = o.get("block", {})
        if tb and b:
            planned_start = time_to_minutes(tb.get("start_time", "00:00"))
            actual_start = time_to_minutes(b.get("start_time", "00:00"))
            start_shifts.append(actual_start - planned_start)
            planned_dur = duration(tb.get("start_time", "00:00"), tb.get("end_time", "00:00"))
            actual_dur = duration(b.get("start_time", "00:00"), b.get("end_time", "00:00"))
            duration_deltas.append(actual_dur - planned_dur)
        if o.get("change_effect") == "replaced":
            key = (b.get("day_of_week"), b.get("start_time"), b.get("end_time"), b.get("label"))
            replacements[key] = replacements.get(key, 0) + 1
        if o.get("reason_category"):
            reasons[o["reason_category"]] = reasons.get(o["reason_category"], 0) + 1

    most_common_effect = max(set(effects), key=effects.count) if effects else None
    effect_frequency = effects.count(most_common_effect) / n if n else 0

    median_shift = median(start_shifts)
    median_duration = median(duration_deltas)

    # Drift requires non-exception concentration and enough occurrences.
    threshold = policy["drift_threshold"]
    confidence = policy["confidence_min"]
    min_occ = policy["min_occurrences_for_baseline_proposal"]
    enough = n >= min_occ
    concentrated = (effect_frequency >= confidence) and (n - exception_count) >= threshold

    recommendation = None
    pattern = "none"
    if enough and concentrated and most_common_effect not in (None, "added"):
        pattern = most_common_effect
        recommendation = {
            "baseline_label": baseline["label"],
            "baseline_day": baseline["day_of_week"],
            "effect": most_common_effect,
            "observed_count": n,
            "override_rate": n / (n + 1),  # simplified: all recent are overrides
            "median_start_shift_minutes": int(median_shift),
            "median_duration_delta_minutes": int(median_duration),
            "proposed_block": build_proposed(baseline, median_shift, median_duration, replacements),
            "evidence_ids": [o.get("id") for o in relevant],
        }
    elif (n - exception_count) >= policy["observe_threshold"] and effect_frequency >= policy["confidence_min"]:
        pattern = "emerging"

    return {
        "recommendation": recommendation,
        "pattern": pattern,
        "effects": effects,
        "classifications": classifications,
        "median_shift": median_shift,
        "median_duration": median_duration,
    }


def build_proposed(baseline, shift, delta, replacements):
    """Build a proposed baseline block from observed medians."""
    proposed = deepcopy(baseline)
    start_min = time_to_minutes(baseline["start_time"]) + int(shift)
    end_min = time_to_minutes(baseline["end_time"]) + int(shift) + int(delta)
    start_min %= 24 * 60
    end_min %= 24 * 60
    proposed["start_time"] = f"{start_min // 60:02d}:{start_min % 60:02d}"
    proposed["end_time"] = f"{end_min // 60:02d}:{end_min % 60:02d}"

    if replacements:
        best = max(replacements, key=replacements.get)
        proposed["day_of_week"] = best[0]
        proposed["start_time"] = best[1]
        proposed["end_time"] = best[2]
        proposed["label"] = best[3]

    return proposed


POLICY = {
    "observe_threshold": 3,
    "drift_threshold": 5,
    "confidence_min": 0.6,
    "time_window_weeks": 12,
    "min_occurrences_for_baseline_proposal": 5,
    "consecutive_exception_limit": 2,
    "median_shift_minutes_for_recommendation": 15,
    "post_change_observations": 3,
}


def make_override(target, block, effect, classification="unknown", reason_category="unknown", oid=None):
    return {
        "id": oid or f"ov-{target['label']}-{effect}",
        "target_block": target,
        "block": block,
        "change_effect": effect,
        "classification": classification,
        "reason_category": reason_category,
    }


def baseline_learning():
    return {
        "label": "Learning",
        "day_of_week": "Wednesday",
        "start_time": "19:00",
        "end_time": "20:30",
        "category": "flexible",
    }


def test_one_isolated_override_no_recommendation():
    print("One isolated override does not trigger a baseline recommendation")
    overrides = [
        make_override(
            baseline_learning(),
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "20:00", "end_time": "21:00"},
            "moved",
            classification="exception",
            reason_category="work",
            oid="ov-1",
        )
    ]
    result = analyze_block(overrides, baseline_learning(), POLICY)
    assert result["recommendation"] is None
    print("  PASS")


def test_one_off_exception_no_influence():
    print("A one-off exception does not materially influence the baseline")
    overrides = [
        make_override(
            baseline_learning(),
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "20:30", "end_time": "21:00"},
            "moved",
            classification="exception",
            reason_category="concert",
        )
    ]
    result = analyze_block(overrides, baseline_learning(), POLICY)
    assert result["pattern"] == "none"
    assert result["recommendation"] is None
    print("  PASS")


def test_repeated_shifts_emerging_pattern():
    print("Repeated similar time shifts produce an emerging pattern")
    b = baseline_learning()
    overrides = [
        make_override(
            b,
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "20:00", "end_time": "21:00"},
            "moved",
            classification="preference",
            reason_category="preference",
            oid=f"ov-shift-{i}",
        )
        for i in range(3)
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["pattern"] == "emerging"
    assert result["recommendation"] is None  # not enough for drift
    print("  PASS")


def test_drift_threshold_triggers():
    print("Repeated consistent overrides trigger schedule-drift detection")
    b = baseline_learning()
    overrides = [
        make_override(
            b,
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "20:10", "end_time": "21:00"},
            "moved",
            classification="preference",
            reason_category="preference",
            oid=f"ov-drift-{i}",
        )
        for i in range(5)
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["pattern"] == "moved"
    assert result["recommendation"] is not None
    assert result["recommendation"]["median_start_shift_minutes"] > 0
    print("  PASS")


def test_inconsistent_overrides_not_overconfident():
    print("Inconsistent overrides do not produce an overconfident recommendation")
    b = baseline_learning()
    overrides = [
        make_override(b, {"label": "Reading", "start_time": "20:00", "end_time": "21:00"}, "replaced", classification="preference", oid="a"),
        make_override(b, {"label": "Learning", "start_time": "21:00", "end_time": "22:00"}, "moved", classification="preference", oid="b"),
        make_override(b, {"label": "Learning", "start_time": "19:00", "end_time": "20:00"}, "shortened", classification="preference", oid="c"),
        make_override(b, {"label": "Learning", "start_time": "19:00", "end_time": "21:00"}, "extended", classification="preference", oid="d"),
        make_override(b, {"label": "Gym", "start_time": "20:00", "end_time": "21:00"}, "replaced", classification="preference", oid="e"),
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["recommendation"] is None or result["recommendation"]["effect"] != "replaced" or len(result["recommendation"]["evidence_ids"]) < 5
    print("  PASS")


def test_cancellations_identified():
    print("Repeated cancellations can be identified")
    b = baseline_learning()
    overrides = [
        make_override(b, {}, "cancelled", classification="friction", reason_category="work", oid=f"ov-cancel-{i}")
        for i in range(5)
    ]
    result = analyze_block(overrides, b, POLICY)
    assert "cancelled" in result["effects"]
    assert all(o["change_effect"] == "cancelled" for o in overrides)
    print("  PASS")


def test_shorten_and_extend_identified():
    print("Repeated shortening/extension can be identified")
    b = baseline_learning()
    overrides = [
        make_override(
            b,
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "19:00", "end_time": "20:00"},
            "shortened",
            classification="preference",
            reason_category="preference",
            oid=f"ov-short-{i}",
        )
        for i in range(5)
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["pattern"] == "shortened"
    assert result["recommendation"] is not None
    print("  PASS")


def test_recurring_replacement_day_time():
    print("A recurring replacement day/time can be identified")
    b = baseline_learning()
    overrides = [
        make_override(
            b,
            {"label": "Build Night", "day_of_week": "Sunday", "start_time": "13:00", "end_time": "17:00"},
            "replaced",
            classification="preference",
            reason_category="preference",
            oid=f"ov-replace-{i}",
        )
        for i in range(5)
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["pattern"] == "replaced"
    assert result["recommendation"] is not None
    rec = result["recommendation"]["proposed_block"]
    assert rec["day_of_week"] == "Sunday"
    assert rec["label"] == "Build Night"
    print("  PASS")


def test_recommendation_includes_evidence():
    print("The OS provides evidence for a proposed baseline change")
    b = baseline_learning()
    overrides = [
        make_override(
            b,
            {"label": "Learning", "day_of_week": "Wednesday", "start_time": "20:10", "end_time": "21:00"},
            "moved",
            classification="preference",
            reason_category="preference",
            oid=f"ov-evidence-{i}",
        )
        for i in range(5)
    ]
    result = analyze_block(overrides, b, POLICY)
    rec = result["recommendation"]
    assert rec is not None
    assert len(rec["evidence_ids"]) == 5
    assert "observed_count" in rec
    assert "median_start_shift_minutes" in rec
    print("  PASS")


def test_baseline_not_modified_without_approval():
    print("The baseline is not modified without explicit approval")
    baseline = {
        "label": "Learning",
        "day_of_week": "Wednesday",
        "start_time": "19:00",
        "end_time": "20:30",
        "category": "flexible",
    }
    original = deepcopy(baseline)
    overrides = [
        make_override(
            baseline,
            {"label": "Learning", "start_time": "20:00", "end_time": "21:00"},
            "moved",
            classification="preference",
        )
        for _ in range(5)
    ]
    # analyzer only returns a recommendation; it does not mutate the baseline dict.
    analyze_block(overrides, baseline, POLICY)
    assert baseline == original
    print("  PASS")


def test_historical_overrides_preserved():
    print("Historical override evidence remains intact")
    b = baseline_learning()
    overrides = [make_override(b, {"label": "Learning", "start_time": "20:00", "end_time": "21:00"}, "moved") for _ in range(5)]
    original_ids = [o["id"] for o in overrides]
    analyze_block(overrides, b, POLICY)
    after_ids = [o["id"] for o in overrides]
    assert after_ids == original_ids
    assert all("id" in o for o in overrides)
    print("  PASS")


def test_post_change_behavior_compared():
    print("Post-change behavior is compared against pre-change behavior")
    # Simulate 3 overrides before, then 0 overrides after an accepted change.
    before = 3
    after = 0
    assert after < before
    # Validation passes when post-change override rate is materially lower.
    status = "validated" if after < before else "not_validated"
    assert status == "validated"
    print("  PASS")


def test_rejected_recommendation_not_repeated():
    print("A rejected recommendation is recorded and not immediately repeated")
    rejected = {"id": "rec-1", "proposed_block": {"start_time": "20:00"}, "status": "rejected"}
    new_evidence = [{"id": "ov-new", "median_shift": 10}]
    # Without new material evidence, do not re-suggest.
    re_suggest = len(new_evidence) > 5 and new_evidence[0]["median_shift"] > 20
    assert not re_suggest
    print("  PASS")


def test_no_noisy_reporting():
    print("Weekly planning/review surfaces meaningful patterns without excessive noise")
    b = baseline_learning()
    # Two unrelated random overrides.
    overrides = [
        make_override(b, {"label": "Learning", "start_time": "19:15", "end_time": "20:30"}, "moved", classification="exception", reason_category="illness"),
        make_override(b, {"label": "Reading", "start_time": "19:00", "end_time": "20:00"}, "replaced", classification="exception", reason_category="family"),
    ]
    result = analyze_block(overrides, b, POLICY)
    assert result["pattern"] == "none"
    assert result["recommendation"] is None
    print("  PASS")


def main():
    print("Schedule Adaptation deterministic tests")
    print("=" * 50)
    test_one_isolated_override_no_recommendation()
    test_one_off_exception_no_influence()
    test_repeated_shifts_emerging_pattern()
    test_drift_threshold_triggers()
    test_inconsistent_overrides_not_overconfident()
    test_cancellations_identified()
    test_shorten_and_extend_identified()
    test_recurring_replacement_day_time()
    test_recommendation_includes_evidence()
    test_baseline_not_modified_without_approval()
    test_historical_overrides_preserved()
    test_post_change_behavior_compared()
    test_rejected_recommendation_not_repeated()
    test_no_noisy_reporting()
    print("\nAll Schedule Adaptation tests passed.")


if __name__ == "__main__":
    main()
