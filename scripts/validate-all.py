#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run schema validation and all deterministic tests.")
    parser.add_argument("--life-root", type=Path, default=ROOT.parent / "ethan-life")
    args = parser.parse_args()

    commands = [
        [sys.executable, str(SCRIPTS / "validate.py"), "--life-root", str(args.life_root.resolve())],
        *[[sys.executable, str(path)] for path in sorted(SCRIPTS.glob("test-*.py"))],
    ]

    failures = []
    for command in commands:
        print(f"\n$ {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            failures.append((command, result.returncode))

    if failures:
        print(f"\n{len(failures)} validation command(s) failed:")
        for command, returncode in failures:
            print(f"  {returncode}: {' '.join(command)}")
        return 1

    print(f"\nAll {len(commands)} validation commands passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
