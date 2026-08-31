#!/usr/bin/env python3
"""
Gym equipment / exercise query tool for Ethan OS.

Demonstrates the health domain equipment/location/exercise model by:
- listing available exercises by muscle or movement
- finding substitutions for unavailable exercises
- temporarily excluding occupied equipment
- building a location-aware workout
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
ETHAN_LIFE = ROOT.parent / "ethan-life"
EXERCISE_LIBRARY = ROOT / "config" / "health" / "exercise-library.yaml"
TAXONOMY = ROOT / "config" / "health" / "equipment-taxonomy.yaml"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

LOADING_ORDER = {"high": 0, "moderate": 1, "low": 2}
SUITABILITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def load_location(location_id: str):
    path = ETHAN_LIFE / "domains" / "health" / "training-locations" / f"{location_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"No training location found: {path}")
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not fm:
        raise ValueError(f"Missing frontmatter in {path}")
    return fm


def load_workout(workout_id: str):
    path = ETHAN_LIFE / "domains" / "health" / "workouts" / f"{workout_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"No workout found: {path}")
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not fm:
        raise ValueError(f"Missing frontmatter in {path}")
    return fm


def load_exercises():
    with EXERCISE_LIBRARY.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("exercises", {})


def equipment_types(location, exclude=None):
    """Return set of canonical equipment type IDs available at the location."""
    exclude = set(exclude or [])
    types = set()
    for item in location.get("equipment", []):
        if item.get("availability") in ("out_of_order", "unknown"):
            continue
        t = item.get("canonical_type")
        if t:
            types.add(t)
    # Bodyweight is available unless this is a no-equipment travel context or explicitly excluded.
    if location.get("location_type") != "travel" and "bodyweight" not in exclude:
        types.add("bodyweight")
    return types - exclude


def available(exercise, available_types):
    if not exercise:
        return False
    required = exercise.get("required_equipment", [])
    return all(eq in available_types for eq in required)


def movement_match_score(original, candidate):
    score = 0
    if candidate.get("movement_pattern") == original.get("movement_pattern"):
        score += 20
    shared_primary = set(candidate.get("primary_muscles", [])) & set(original.get("primary_muscles", []))
    score += len(shared_primary) * 5
    return score


def best_substitute(exercise_id, exercises, available_types, original=None):
    """Find the best available substitute for an exercise."""
    original = original or exercises.get(exercise_id)
    if not original:
        return None

    # 1. Preferred ordered substitutes
    for sub in original.get("substitutes", []):
        sid = sub["exercise_id"] if isinstance(sub, dict) else sub
        candidate = exercises.get(sid)
        if candidate and available(candidate, available_types):
            return candidate

    # 2. Fallback: same movement pattern + overlapping primary muscles
    fallback = []
    for eid, candidate in exercises.items():
        if eid == exercise_id:
            continue
        if not available(candidate, available_types):
            continue
        if candidate.get("cardio"):
            continue
        score = movement_match_score(original, candidate)
        if score >= 20:  # same movement pattern at minimum
            fallback.append((score, candidate))

    if not fallback:
        return None

    # Prefer higher loading, better strength/hypertrophy suitability, non-isolation for compounds
    def sort_key(item):
        score, c = item
        loading = LOADING_ORDER.get(c.get("loading_potential", "low"), 99)
        strength = SUITABILITY_ORDER.get(c.get("strength_suitability", "low"), 99)
        hypertrophy = SUITABILITY_ORDER.get(c.get("hypertrophy_suitability", "low"), 99)
        isolation = 1 if c.get("isolation") else 0
        return (-score, loading, -isolation, strength, hypertrophy)

    fallback.sort(key=sort_key)
    return fallback[0][1]


def list_by_muscle(muscle, exercises, available_types):
    results = []
    for eid, ex in exercises.items():
        if ex.get("cardio"):
            continue
        if muscle in ex.get("primary_muscles", []):
            if available(ex, available_types):
                results.append((eid, ex))
    return results


def choose_for_muscle(muscle, exercises, available_types, allow_isolation=False, used=None):
    used = set(used or [])
    candidates = []
    for eid, ex in exercises.items():
        if eid in used:
            continue
        if ex.get("cardio"):
            continue
        if muscle in ex.get("primary_muscles", []):
            if not available(ex, available_types):
                continue
            loading = LOADING_ORDER.get(ex.get("loading_potential", "low"), 99)
            strength = SUITABILITY_ORDER.get(ex.get("strength_suitability", "low"), 99)
            hypertrophy = SUITABILITY_ORDER.get(ex.get("hypertrophy_suitability", "low"), 99)
            isolation = 0 if allow_isolation or not ex.get("isolation") else 1
            # Prefer compound movements for larger muscle groups
            if muscle in ("chest", "lats", "rhomboids", "shoulders") and ex.get("isolation"):
                isolation = 1  # lower priority
            candidates.append((isolation, loading, strength, hypertrophy, eid, ex))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0]


def build_workout(duration_min, location, exercises, available_types):
    targets = [
        ("chest", False),
        ("lats", False),
        ("rhomboids", False),
        ("shoulders", False),
        ("quadriceps", False),
        ("hamstrings", False),
        ("glutes", False),
        ("calves", True),
        ("biceps", True),
        ("triceps", True),
        ("core", True),
    ]
    blocks = []
    used = set()
    for muscle, allow_iso in targets:
        chosen = choose_for_muscle(muscle, exercises, available_types, allow_iso, used)
        if chosen:
            _, _, _, _, eid, ex = chosen
            used.add(eid)
            if ex.get("isolation"):
                sets, reps, rest = 3, "12-15", "60s"
            elif ex.get("strength_suitability") == "high":
                sets, reps, rest = 3, "5", "120s"
            else:
                sets, reps, rest = 3, "8-10", "90s"
            blocks.append({
                "exercise_id": eid,
                "title": ex["title"],
                "sets": sets,
                "reps": reps,
                "rest": rest,
                "primary_muscles": ex.get("primary_muscles", []),
            })

    # Trim to fit duration if needed (rough estimate)
    per_exercise_min = 7
    max_blocks = max(2, duration_min // per_exercise_min)
    return blocks[:max_blocks], duration_min


def format_exercise(eid, ex):
    return f"  {eid:<35} {ex['title']:<35} {ex.get('loading_potential','?')} load | {ex.get('stability','?')}"


def main():
    parser = argparse.ArgumentParser(description="Query Ethan OS gym/equipment data.")
    parser.add_argument("--location", default="apartment-gym", help="Training location ID")
    parser.add_argument("--exclude", action="append", default=[], help="Equipment type to temporarily exclude")
    parser.add_argument("--muscle", help="List available exercises for a primary muscle")
    parser.add_argument("--hamstring", action="store_true", help="List hamstring exercises")
    parser.add_argument("--chest", action="store_true", help="List chest exercises")
    parser.add_argument("--exercise", help="Check a specific exercise")
    parser.add_argument("--substitute", action="store_true", help="Suggest a substitute for the given exercise")
    parser.add_argument("--build", type=int, help="Build a workout of given duration (minutes)")
    parser.add_argument("--workout", help="Check feasibility of a workout object by id")
    args = parser.parse_args()

    location = load_location(args.location)
    exercises = load_exercises()
    available_types = equipment_types(location, exclude=args.exclude)

    if args.chest:
        args.muscle = "chest"
    if args.hamstring:
        args.muscle = "hamstrings"

    if args.muscle:
        results = list_by_muscle(args.muscle, exercises, available_types)
        if not results:
            print(f"No available {args.muscle} exercises at {location['name']}.")
            return
        print(f"Available {args.muscle} exercises at {location['name']}:")
        for eid, ex in sorted(results, key=lambda x: x[1]["title"]):
            print(format_exercise(eid, ex))
        return

    if args.exercise:
        ex = exercises.get(args.exercise)
        if not ex:
            print(f"Unknown exercise: {args.exercise}")
            return
        if available(ex, available_types):
            print(f"{ex['title']} is available at {location['name']}.")
            if args.substitute:
                sub = best_substitute(args.exercise, exercises, available_types, ex)
                if sub:
                    print(f"Closest substitute: {sub['title']}")
                else:
                    print("No substitute found.")
        else:
            print(f"{ex['title']} is NOT available at {location['name']}.")
            sub = best_substitute(args.exercise, exercises, available_types, ex)
            if sub:
                print(f"Closest substitute: {sub['title']}")
            else:
                print("No substitute found.")
        return

    if args.build:
        blocks, duration = build_workout(args.build, location, exercises, available_types)
        print(f"{duration}-minute workout at {location['name']}:")
        print(f"{'#':<3} {'Exercise':<35} {'Sets':<5} {'Reps':<8} {'Rest':<6}")
        for i, b in enumerate(blocks, 1):
            print(f"{i:<3} {b['title']:<35} {b['sets']:<5} {b['reps']:<8} {b['rest']:<6}")
        return

    if args.workout:
        workout = load_workout(args.workout)
        print(f'Feasibility check for "{workout.get("title", args.workout)}" at {location["name"]}:' )
        print(f"{'#':<3} {'Planned':<35} {'Status':<15} {'Action / Substitute':<35}")
        all_ok = True
        for i, block in enumerate(workout.get("blocks", []), 1):
            eid = block["exercise_id"]
            ex = exercises.get(eid)
            if not ex:
                status = "UNKNOWN"
                sub_title = "not in library"
            elif available(ex, available_types):
                status = "OK"
                sub_title = "-"
            else:
                status = "NOT AVAILABLE"
                sub = best_substitute(eid, exercises, available_types, ex)
                sub_title = sub["title"] if sub else "no substitute"
                all_ok = False
            print(f"{i:<3} {ex['title'] if ex else eid:<35} {status:<15} {sub_title:<35}")
        if all_ok:
            print("\nAll planned exercises are available at this location.")
        else:
            print("\nSome exercises are not available. Substitutes listed above.")
        return

    # Default: show location summary
    print(f"Location: {location['name']} ({location['location_type']})")
    print(f"Audit date: {location.get('audit_date', 'unknown')}")
    print(f"Available equipment: {', '.join(sorted(available_types))}")
    total = sum(1 for ex in exercises.values() if available(ex, available_types))
    print(f"Exercises available: {total}/{len(exercises)}")


if __name__ == "__main__":
    main()
