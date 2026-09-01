#!/usr/bin/env python3
"""
Apply the downstream identity layer to user-facing content.

This script reads the central identity/framework configuration from
config/ethan-os.config.yaml and rewrites personalizable Markdown/YAML files so
that the downstream OS presents itself as the owner's OS (e.g., John OS) while
leaving all upstream framework provenance intact.

Protected provenance is never rewritten: LICENSE, NOTICE, .os-upstream.yaml,
framework config, the upstream Git remote, and the framework identifiers in
config/ethan-os.config.yaml.

Run from inside the downstream OS repository:
    python scripts/personalize.py

It is idempotent: running it again will not corrupt already-personalized files
as long as the identity has not changed.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path("config") / "ethan-os.config.yaml"

# Paths and roots that are protected provenance.
PROTECTED_FILES = {
    ".os-upstream.yaml",
    "LICENSE",
    "NOTICE",
    "config/ethan-os.config.yaml",
    "runtime/manifest.yaml",
    "config/downstream-manifest.template.yaml",
    "docs/README.md",
    "docs/VISION.md",
    "docs/RELEASES.md",
    "docs/ROADMAP.md",
    "docs/project-naming.md",
}

PROTECTED_DIRS = {
    ".git",
    "adapters",
    "schemas",
    "scripts",
    "core",                 # workflows/core, skills/core
    "getting-started",
    "concepts",
    "architecture",
    "runtime",
}

# Roots that contain user-facing text. Everything under these is considered,
# unless explicitly protected by PROTECTED_FILES/PROTECTED_DIRS.
PERSONALIZE_ROOTS = {
    "docs",
    "workflows",
    "skills",
    "instructions",
    "entrypoint",
    "config/health",
    "README.md",
}


class Personalizer:
    def __init__(self, repo: Path, identity: dict, framework: dict):
        self.repo = Path(repo).resolve()
        self.owner = identity["owner_name"]
        self.os = identity["os_name"]
        self.os_repo = identity["os_repo"]
        self.life_repo = identity["life_repo"]
        self.framework_name = framework["name"]
        self.framework_id = framework["id"]

    def _is_protected(self, path: Path) -> bool:
        rel = path.relative_to(self.repo).as_posix()
        if rel in PROTECTED_FILES:
            return True
        for part in path.relative_to(self.repo).parts:
            if part in PROTECTED_DIRS:
                return True
        return False

    def _provenance_guard(self, line: str) -> bool:
        """Return True if a line should not be modified because it carries provenance."""
        # Keep any line that already refers to the framework as an upstream link,
        # e.g., "built from [Ethan OS](...)" or uses framework identifiers.
        if self.framework_name in line:
            # Markdown link containing the framework name is attribution.
            if re.search(rf"\[.*?{re.escape(self.framework_name)}.*?\]", line):
                return True
            # Any mention of the framework id / upstream repo keeps the framework name.
            if self.framework_id in line or "upstream" in line.lower() or ".git" in line:
                return True
        # Code blocks are left as-is to avoid breaking identifiers.
        if line.lstrip().startswith("```") or line.lstrip().startswith("    "):
            return False  # we still want to scan inside code? Safer to leave it alone.
        return False

    def _transform_line(self, line: str) -> str:
        if self._provenance_guard(line):
            return line

        # Order matters: product name first, then the companion repo name, then the
        # bare owner name. The framework id (ethan-os) is left intact as provenance.
        line = re.sub(rf"\b{re.escape(self.framework_name)}\b", self.os, line)
        line = re.sub(rf"\bethan-life\b", self.life_repo, line)
        # Only replace the bare owner name, not a hyphenated compound like ethan-os-life.
        line = re.sub(rf"\bEthan\b(?!-)", self.owner, line)
        return line

    def _transform(self, text: str) -> str:
        out = []
        in_code_block = False
        for line in text.splitlines(keepends=True):
            stripped = line.lstrip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                out.append(line)
                continue
            if in_code_block:
                out.append(line)
                continue
            out.append(self._transform_line(line))
        return "".join(out)

    def personalize_file(self, path: Path):
        if self._is_protected(path):
            return False
        text = path.read_text(encoding="utf-8")
        transformed = self._transform(text)
        if transformed == text:
            return False
        path.write_text(transformed, encoding="utf-8")
        return True

    def personalize_repo(self, dry_run: bool = False):
        touched = []
        for path in self._walk():
            if dry_run:
                text = path.read_text(encoding="utf-8")
                if self._transform(text) != text:
                    touched.append(str(path.relative_to(self.repo).as_posix()))
            else:
                if self.personalize_file(path):
                    touched.append(str(path.relative_to(self.repo).as_posix()))
        return touched

    def _walk(self):
        # Walk personalizable roots and then any root-level README.md.
        results = []
        for name in PERSONALIZE_ROOTS:
            p = self.repo / name
            if p.is_dir():
                for child in p.rglob("*"):
                    if child.is_file() and child.suffix in {".md", ".yaml"}:
                        results.append(child)
            elif p.is_file():
                results.append(p)
        return results


def load_config(repo: Path):
    path = repo / CONFIG_PATH
    if not path.exists():
        raise RuntimeError(f"{CONFIG_PATH} not found. Is this an OS repository?")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("identity"), data.get("framework")


def main():
    parser = argparse.ArgumentParser(description="Apply downstream identity to user-facing content.")
    parser.add_argument("--repo-dir", default=".", help="Path to the OS repository.")
    parser.add_argument("--list", action="store_true", help="Show which files would be touched without writing.")
    args = parser.parse_args()

    repo = Path(args.repo_dir).resolve()
    identity, framework = load_config(repo)
    if not identity or not framework:
        print(f"ERROR: {CONFIG_PATH} must contain 'identity' and 'framework' sections.")
        return 1

    personalizer = Personalizer(repo, identity, framework)

    if args.list:
        touched = personalizer.personalize_repo(dry_run=True)
        print("Files that would be personalized:")
        for t in touched:
            print(f"  {t}")
        return 0

    touched = personalizer.personalize_repo()
    if touched:
        print("Personalized files:")
        for t in touched:
            print(f"  {t}")
    else:
        print("No files needed personalization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
