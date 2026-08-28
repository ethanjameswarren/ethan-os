#!/usr/bin/env python3
"""
End-to-end demo flow for Ethan OS.

Reads version from the repository VERSION file.

Simulates:
  capture -> process learning notes -> extract ideas -> relationships
  -> summary -> review -> retrieve

Uses the demo personality fixtures.
"""

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
FIXTURES = ROOT / "config" / "demo-personality" / "fixtures"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def load_objects(folder: Path):
    objects = {}
    for path in folder.rglob("*.md"):
        if path.name == "README.md":
            continue
        fm, text = parse_frontmatter(path)
        if fm and "id" in fm:
            objects[fm["id"]] = {"fm": fm, "text": text, "path": path}
    return objects


def main():
    print(f"Ethan OS {VERSION} End-to-End Demo")
    print("=" * 50)

    # 1. Capture
    capture_path = FIXTURES / "domains" / "knowledge" / "captures" / "capture-2026-01-15-atomic-habits-ch4.md"
    fm, text = parse_frontmatter(capture_path)
    print("\n[1] CAPTURE")
    print(f"  ID: {fm['id']}")
    print(f"  Title: {fm['title']}")
    print(f"  Source: {fm.get('source_id')}")

    # 2. Source
    source_path = FIXTURES / "domains" / "knowledge" / "sources" / "book-atomic-habits.md"
    fm_src, _ = parse_frontmatter(source_path)
    print("\n[2] SOURCE")
    print(f"  ID: {fm_src['id']}")
    print(f"  Title: {fm_src['title']}")
    print(f"  Type: {fm_src['source_type']}")

    # 3. Ideas
    ideas_dir = FIXTURES / "domains" / "knowledge" / "ideas"
    ideas = load_objects(ideas_dir)
    print("\n[3] IDEAS")
    for iid, obj in ideas.items():
        print(f"  - {iid}: {obj['fm']['title']}")
        print(f"      position={obj['fm'].get('position')} confidence={obj['fm'].get('confidence')}")

    # 4. Relationships
    print("\n[4] RELATIONSHIPS")
    link_count = 0
    for iid, obj in ideas.items():
        for link in obj["fm"].get("links", []):
            link_count += 1
            print(f"  - {iid} --[{link['relation']}]--> {link['target']}")
    print(f"  Total typed relationships: {link_count}")

    # 5. Summary
    summary_path = FIXTURES / "domains" / "knowledge" / "summaries" / "atomic-habits.md"
    fm_sum, text_sum = parse_frontmatter(summary_path)
    print("\n[5] SUMMARY")
    print(f"  ID: {fm_sum['id']}")
    print(f"  Source: {fm_sum.get('source_id')}")
    print(f"  Has 30 Seconds section: {'## 30 Seconds' in text_sum}")
    print(f"  Has 5 Minutes section: {'## 5 Minutes' in text_sum}")
    print(f"  Has Detailed section: {'## Detailed Personal Summary' in text_sum}")
    print(f"  Contains personal interpretation: {'My interpretation' in text_sum}")
    print(f"  Contains disagreement: {'disagree' in text_sum.lower()}")

    # 6. Review
    review_path = FIXTURES / "domains" / "knowledge" / "reviews" / "review-2026-q1.md"
    fm_rev, _ = parse_frontmatter(review_path)
    print("\n[6] REVIEW")
    print(f"  ID: {fm_rev['id']}")
    print(f"  Targets: {fm_rev.get('target_ids')}")

    # 7. Retrieve (simulated)
    print("\n[7] RETRIEVE: What have I learned about motivation?")
    relevant = [
        (iid, obj)
        for iid, obj in ideas.items()
        if any(word in obj["text"].lower() for word in ["habit", "system", "identity", "goal"])
    ]
    print(f"  Found {len(relevant)} relevant ideas:")
    for iid, obj in relevant:
        print(f"  - {iid}: {obj['fm']['title']}")

    print("\nDemo flow complete.")


if __name__ == "__main__":
    main()
