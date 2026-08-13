#!/usr/bin/env python3
"""
Deterministic validation for Ethan OS v0.1.

Checks:
- valid YAML frontmatter
- schema identifier resolves in registry
- required fields present
- provenance present
- relationship target IDs exist
- duplicate IDs not created
- supported schema versions
"""

import os
import re
import sys
from pathlib import Path

# Try PyYAML; if missing, use a minimal frontmatter parser
try:
    import yaml
    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_REGISTRY = ROOT / "schemas" / "registry.yaml"

DEMO_FIXTURES = ROOT / "config" / "demo-personality" / "fixtures"
ETHAN_LIFE = ROOT.parent / "ethan-life"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    fm_text = match.group(1)
    if HAS_YAML:
        return yaml.safe_load(fm_text)
    raise RuntimeError("PyYAML is required for validation.")


def load_registry():
    with SCHEMA_REGISTRY.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("schemas", {})


def find_markdown_files(base: Path):
    if not base.exists():
        return []
    return sorted(base.rglob("*.md"))


def relative_path(path: Path) -> str:
    if str(path).startswith(str(ROOT)):
        return path.relative_to(ROOT).as_posix()
    return path.relative_to(ETHAN_LIFE).as_posix()


def validate_object(path: Path, registry: dict, all_ids: dict, broken: list):
    rel = relative_path(path)
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm is None:
        # README and plain docs may not have frontmatter; skip object validation
        if path.name != "README.md" and "domains" in path.parts:
            broken.append(f"{rel}: missing frontmatter")
        return

    # Required fields
    for field in ("id", "schema", "schema_version", "title", "created_at"):
        if field not in fm:
            broken.append(f"{rel}: missing required field '{field}'")

    obj_id = fm.get("id")
    schema_key = fm.get("schema")
    version = fm.get("schema_version")

    if obj_id and obj_id in all_ids and all_ids[obj_id] != rel:
        broken.append(f"{rel}: duplicate id '{obj_id}' also in {all_ids[obj_id]}")

    if schema_key:
        if schema_key not in registry:
            broken.append(f"{rel}: unknown schema '{schema_key}'")
        else:
            entry = registry[schema_key]
            supported = entry.get("version")
            if version != supported:
                broken.append(
                    f"{rel}: schema version {version} != registry version {supported}"
                )
            schema_file = ROOT / "schemas" / entry.get("file")
            if not schema_file.exists():
                broken.append(f"{rel}: schema file missing '{entry.get('file')}'")

    # Provenance presence
    if "provenance" not in fm:
        broken.append(f"{rel}: missing provenance")
    elif not isinstance(fm.get("provenance"), dict):
        broken.append(f"{rel}: provenance is not a mapping")

    # Relationship target existence
    links = fm.get("links", [])
    if links:
        if not isinstance(links, list):
            broken.append(f"{rel}: links is not a list")
        else:
            for link in links:
                target = link.get("target")
                relation = link.get("relation")
                if not target:
                    broken.append(f"{rel}: link missing target")
                if target and target not in all_ids:
                    # target may appear later; defer check to second pass
                    pass
                if not relation:
                    broken.append(f"{rel}: link missing relation")


def main():
    print("Ethan OS v0.1 deterministic validation")
    print("=" * 40)

    if not HAS_YAML:
        print("ERROR: PyYAML is required. Install with: pip install pyyaml")
        sys.exit(1)

    registry = load_registry()
    print(f"Loaded schema registry with {len(registry)} schemas")

    broken = []
    all_ids = {}

    # Pass 1: collect IDs
    files = []
    files.extend(find_markdown_files(DEMO_FIXTURES))
    files.extend(find_markdown_files(ETHAN_LIFE))

    for path in files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm and "id" in fm:
            rel = path.relative_to(ROOT if str(path).startswith(str(ROOT)) else ETHAN_LIFE).as_posix()
            obj_id = fm["id"]
            if obj_id in all_ids:
                broken.append(f"{rel}: duplicate id '{obj_id}' also in {all_ids[obj_id]}")
            else:
                all_ids[obj_id] = rel

    # Pass 2: full validation
    for path in files:
        validate_object(path, registry, all_ids, broken)

    # Pass 3: relationship targets
    for path in files:
        rel = path.relative_to(ROOT if str(path).startswith(str(ROOT)) else ETHAN_LIFE).as_posix()
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            continue
        for link in fm.get("links", []):
            target = link.get("target")
            if target and target not in all_ids:
                broken.append(f"{rel}: broken link to unknown id '{target}'")

    print(f"Checked {len(files)} Markdown files")

    if broken:
        print(f"\nFAILURES ({len(broken)}):")
        for item in broken:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("\nAll deterministic checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
