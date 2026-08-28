#!/usr/bin/env python3
"""
Deterministic tests for the Context Engine foundation contracts.

Checks:
- core.context-request and core.context-bundle are registered
- schema files exist and are well-formed YAML
- required fields are present
- the context-assembly skill and doc reference the bundle schema
"""

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


def main():
    print("Context Engine contract tests")
    print("=" * 40)

    broken = []

    registry_path = ROOT / "schemas" / "registry.yaml"
    if not registry_path.exists():
        broken.append("schemas/registry.yaml not found")
    else:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        schemas = registry.get("schemas", {})
        if "core.context-request" not in schemas:
            broken.append("core.context-request not in schemas/registry.yaml")
        if "core.context-bundle" not in schemas:
            broken.append("core.context-bundle not in schemas/registry.yaml")

    req_schema = ROOT / "schemas" / "core" / "context-request.schema.yaml"
    bundle_schema = ROOT / "schemas" / "core" / "context-bundle.schema.yaml"

    for path in [req_schema, bundle_schema]:
        if not path.exists():
            broken.append(f"{path} not found")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as e:
            broken.append(f"{path} is not valid YAML: {e}")
            continue
        if not isinstance(data, dict):
            broken.append(f"{path} is not a mapping")
            continue
        required = data.get("required", [])
        if path.name == "context-request.schema.yaml":
            if "intent" not in required:
                broken.append("context-request missing required 'intent'")
            if "domains" not in required:
                broken.append("context-request missing required 'domains'")
        if path.name == "context-bundle.schema.yaml":
            if "request" not in required:
                broken.append("context-bundle missing required 'request'")
            if "assembled_at" not in required:
                broken.append("context-bundle missing required 'assembled_at'")

    skill = ROOT / "skills" / "core" / "context-assembly.md"
    if not skill.exists():
        broken.append("skills/core/context-assembly.md not found")
    else:
        skill_text = skill.read_text(encoding="utf-8")
        if "core.context-request" not in skill_text or "core.context-bundle" not in skill_text:
            broken.append("context-assembly skill does not reference the contract schemas")

    doc = ROOT / "docs" / "architecture" / "context-assembly.md"
    if not doc.exists():
        broken.append("docs/architecture/context-assembly.md not found")
    else:
        if "core.context-request" not in doc.read_text(encoding="utf-8"):
            broken.append("context-assembly doc does not reference core.context-request")

    if broken:
        print(f"\nFAILURES ({len(broken)}):")
        for item in broken:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("\nAll Context Engine contract tests passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
