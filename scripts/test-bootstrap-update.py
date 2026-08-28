#!/usr/bin/env python3
"""
Deterministic tests for downstream bootstrap and safe upstream updates.

Uses synthetic upstream/downstream repositories in a temporary directory.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Test User",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test User",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


def run(cmd, cwd=None, check=True, env=GIT_ENV):
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        env=env,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n{result.stdout}\n{result.stderr}"
        )
    return result


def run_git(*args, cwd=None, check=True):
    return run(["git", *args], cwd=cwd, check=check, env=GIT_ENV).stdout.strip()


def make_upstream(tmp: Path) -> Path:
    up = tmp / "ethan-os"
    up.mkdir(parents=True, exist_ok=True)
    (up / "VERSION").write_text("0.1.0\n")
    (up / "README.md").write_text("# Ethan OS\n\nUpstream project.\n")
    (up / "config").mkdir()
    (up / "config" / "ethan-os.config.yaml").write_text(
        "ethan_os:\n  name: Ethan OS\n  version: 0.1.0\n  default_domain: knowledge\n"
    )
    (up / "schemas").mkdir()
    (up / "schemas" / "registry.yaml").write_text("schemas: {}\n")
    (up / "scripts").mkdir()
    (up / "scripts" / "validate.py").write_text(
        "import sys\nif __name__ == '__main__':\n    sys.exit(0)\n"
    )
    (up / "LICENSE").write_text("Apache License 2.0\n")
    (up / "NOTICE").write_text("Ethan OS\nCopyright 2026 Ethan OS authors\n")
    run_git("init", cwd=up)
    run_git("add", ".", cwd=up)
    run_git("commit", "-m", "Initial upstream", cwd=up)
    return up


def bootstrap(upstream: Path, downstream: Path, name: str, identifier: str) -> Path:
    script = Path(__file__).resolve().parent / "bootstrap-personal-os.py"
    run(
        [
            sys.executable,
            str(script),
            "--target-dir",
            str(downstream),
            "--os-name",
            name,
            "--identifier",
            identifier,
            "--upstream-repo",
            str(upstream),
        ],
        check=True,
    )
    return downstream


def update(downstream: Path, apply: bool = False, check: bool = True):
    script = Path(__file__).resolve().parent / "update-from-upstream.py"
    args = [sys.executable, str(script)]
    if apply:
        args.append("--apply")
    result = run(args, cwd=downstream, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"update-from-upstream failed:\n{result.stdout}\n{result.stderr}"
        )
    return result


def test_scenario_a_clean_update(tmp: Path):
    print("Scenario A — clean update")
    up = make_upstream(tmp / "up-a")
    ds = bootstrap(up, tmp / "john-a", "John OS", "john-os")

    # Modify an upstream file that bootstrap does not touch.
    (up / "schemas" / "registry.yaml").write_text("schemas:\n  x: {}\n")
    run_git("add", "schemas/registry.yaml", cwd=up)
    run_git("commit", "-m", "Update registry", cwd=up)

    result = update(ds, apply=True)
    assert "Safe updates: 1" in result.stdout or "safe updates: 1" in result.stdout.lower()
    assert (ds / "schemas" / "registry.yaml").read_text() == (up / "schemas" / "registry.yaml").read_text()
    print("  PASS")


def test_scenario_b_downstream_only_preserved(tmp: Path):
    print("Scenario B — downstream-only file preserved")
    up = make_upstream(tmp / "up-b")
    ds = bootstrap(up, tmp / "john-b", "John OS", "john-os")

    (ds / "workflows").mkdir()
    (ds / "workflows" / "home" / "garden.md").write_text("# Garden planning\n") if False else None
    # Create nested file.
    (ds / "workflows" / "home").mkdir(exist_ok=True)
    (ds / "workflows" / "home" / "garden.md").write_text("# Garden planning\n")
    run_git("add", ".", cwd=ds)
    run_git("commit", "-m", "Add garden workflow", cwd=ds)

    # Modify upstream.
    (up / "README.md").write_text("# Ethan OS\n\nUpdated.\n")
    run_git("add", "README.md", cwd=up)
    run_git("commit", "-m", "Update README", cwd=up)

    update(ds, apply=True)
    assert (ds / "workflows" / "home" / "garden.md").exists()
    print("  PASS")


def test_scenario_c_conflict(tmp: Path):
    print("Scenario C — upstream + downstream modify same file")
    up = make_upstream(tmp / "up-c")
    ds = bootstrap(up, tmp / "john-c", "John OS", "john-os")

    # Downstream modifies README.
    (ds / "README.md").write_text("# John OS\n\nJohn's version.\n")
    run_git("add", "README.md", cwd=ds)
    run_git("commit", "-m", "Customize README", cwd=ds)

    # Upstream also modifies README.
    (up / "README.md").write_text("# Ethan OS\n\nUpstream version 2.\n")
    run_git("add", "README.md", cwd=up)
    run_git("commit", "-m", "Update upstream README", cwd=up)

    result = update(ds, apply=False)
    assert "Conflicts requiring review: 1" in result.stdout
    assert "README.md" in result.stdout

    # Apply should not overwrite the downstream README.
    update(ds, apply=True)
    text = (ds / "README.md").read_text()
    assert "John's version" in text
    print("  PASS")


def test_scenario_e_upstream_delete_downstream_modify(tmp: Path):
    print("Scenario E — upstream deletes file modified downstream")
    up = make_upstream(tmp / "up-e")
    ds = bootstrap(up, tmp / "john-e", "John OS", "john-os")

    # Create a file upstream and downstream modifies it.
    (up / "docs").mkdir(exist_ok=True)
    (up / "docs" / "old.md").write_text("# Old\n")
    run_git("add", "docs/old.md", cwd=up)
    run_git("commit", "-m", "Add old doc", cwd=up)

    # Bootstrap a fresh downstream that includes the new file in its base.
    ds2 = bootstrap(up, tmp / "john-e2", "John OS", "john-os")
    ds = ds2

    (ds / "docs" / "old.md").write_text("# Old\n\nJohn's additions.\n")
    run_git("add", "docs/old.md", cwd=ds)
    run_git("commit", "-m", "Customize old doc", cwd=ds)

    # Upstream deletes it.
    os.remove(up / "docs" / "old.md")
    run_git("rm", "docs/old.md", cwd=up)
    run_git("commit", "-m", "Remove old doc", cwd=up)

    result = update(ds, apply=True)
    assert (ds / "docs" / "old.md").exists()
    assert "removal conflict" in result.stdout.lower()
    print("  PASS")


def test_scenario_f_new_upstream_capability(tmp: Path):
    print("Scenario F — new upstream file added")
    up = make_upstream(tmp / "up-f")
    ds = bootstrap(up, tmp / "john-f", "John OS", "john-os")

    (up / "docs" / "capabilities").mkdir(parents=True, exist_ok=True)
    (up / "docs" / "capabilities" / "schedule-planning.md").write_text("# Schedule Planning\n")
    run_git("add", ".", cwd=up)
    run_git("commit", "-m", "Add schedule planning doc", cwd=up)

    update(ds, apply=True)
    assert (ds / "docs" / "capabilities" / "schedule-planning.md").exists()
    print("  PASS")


def test_scenario_h_failed_validation(tmp: Path):
    print("Scenario H — validation fails after update")
    up = make_upstream(tmp / "up-h")
    ds = bootstrap(up, tmp / "john-h", "John OS", "john-os")

    # Upstream change that will make validate.py fail.
    (up / "BREAK_VALIDATION").write_text("break\n")
    run_git("add", "BREAK_VALIDATION", cwd=up)
    run_git("commit", "-m", "Break validation", cwd=up)

    # Make downstream validate.py fail when marker file exists.
    (ds / "scripts" / "validate.py").write_text(
        "import sys, os\nif os.path.exists('BREAK_VALIDATION'): sys.exit(1)\nsys.exit(0)\n"
    )
    run_git("add", "scripts/validate.py", cwd=ds)
    run_git("commit", "-m", "Add validation guard", cwd=ds)

    # Upstream validate.py is still the simple success script, but the marker file will be added.
    result = update(ds, apply=True, check=False)
    assert result.returncode != 0 or "Validation failed" in result.stdout
    assert (ds / "BREAK_VALIDATION").exists()  # file was checked out by apply
    # Manifest should not record successful update because commit failed before manifest update.
    print("  PASS")


def test_scenario_i_bootstrap_preserves_legal_artifacts(tmp: Path):
    print("Scenario I — bootstrap preserves LICENSE, NOTICE, and attribution")
    up = make_upstream(tmp / "up-i")
    ds = bootstrap(up, tmp / "john-i", "John OS", "john-os")

    assert (ds / "LICENSE").exists()
    assert (ds / "NOTICE").exists()
    assert "Ethan OS" in (ds / "NOTICE").read_text()
    assert "Apache" in (ds / "LICENSE").read_text()

    # README should use John OS as the project name but still attribute upstream.
    readme = (ds / "README.md").read_text()
    assert readme.startswith("# John OS")
    assert "Ethan OS" in readme
    print("  PASS")


def test_scenario_j_downstream_notice_survives_update(tmp: Path):
    print("Scenario J — downstream NOTICE additions survive an update")
    up = make_upstream(tmp / "up-j")
    ds = bootstrap(up, tmp / "john-j", "John OS", "john-os")

    # John adds her own attribution section.
    notice = (ds / "NOTICE").read_text()
    (ds / "NOTICE").write_text(notice + "\nJohn OS\nCopyright 2026 John\n")
    run_git("add", "NOTICE", cwd=ds)
    run_git("commit", "-m", "Add downstream notice", cwd=ds)

    # Upstream changes an unrelated file.
    (up / "schemas" / "registry.yaml").write_text("schemas:\n  y: {}\n")
    run_git("add", "schemas/registry.yaml", cwd=up)
    run_git("commit", "-m", "Update registry", cwd=up)

    update(ds, apply=True)
    ds_notice = (ds / "NOTICE").read_text()
    assert "Ethan OS" in ds_notice
    assert "John OS" in ds_notice
    print("  PASS")


def test_scenario_k_upstream_notice_change_flags_conflict(tmp: Path):
    print("Scenario K — upstream NOTICE change is flagged when downstream also changed it")
    up = make_upstream(tmp / "up-k")
    ds = bootstrap(up, tmp / "john-k", "John OS", "john-os")

    # Downstream adds a notice.
    notice = (ds / "NOTICE").read_text()
    (ds / "NOTICE").write_text(notice + "\nJohn OS additions\n")
    run_git("add", "NOTICE", cwd=ds)
    run_git("commit", "-m", "Add downstream notice", cwd=ds)

    # Upstream changes NOTICE.
    (up / "NOTICE").write_text("Ethan OS\nCopyright 2026 Ethan OS authors\nUpdated upstream notice.\n")
    run_git("add", "NOTICE", cwd=up)
    run_git("commit", "-m", "Update NOTICE", cwd=up)

    result = update(ds, apply=False)
    assert "NOTICE" in result.stdout
    assert "legal/project-lineage conflict" in result.stdout
    # Apply should leave downstream NOTICE intact because it is a conflict.
    update(ds, apply=True)
    assert "John OS additions" in (ds / "NOTICE").read_text()
    print("  PASS")


def test_scenario_l_upstream_license_change_flagged(tmp: Path):
    print("Scenario L — upstream LICENSE change is flagged as a legal change")
    up = make_upstream(tmp / "up-l")
    ds = bootstrap(up, tmp / "john-l", "John OS", "john-os")

    # Upstream changes LICENSE.
    (up / "LICENSE").write_text("Apache License 2.0\nUpdated license text.\n")
    run_git("add", "LICENSE", cwd=up)
    run_git("commit", "-m", "Update LICENSE", cwd=up)

    result = update(ds, apply=True)
    assert "LICENSE" in result.stdout
    assert "legal/project-lineage" in result.stdout.lower()
    assert "Apache" in (ds / "LICENSE").read_text()
    print("  PASS")


def main():
    print("Bootstrap/Update deterministic tests")
    print("=" * 50)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        test_scenario_a_clean_update(tmp)
        test_scenario_b_downstream_only_preserved(tmp)
        test_scenario_c_conflict(tmp)
        test_scenario_e_upstream_delete_downstream_modify(tmp)
        test_scenario_f_new_upstream_capability(tmp)
        test_scenario_h_failed_validation(tmp)
        test_scenario_i_bootstrap_preserves_legal_artifacts(tmp)
        test_scenario_j_downstream_notice_survives_update(tmp)
        test_scenario_k_upstream_notice_change_flags_conflict(tmp)
        test_scenario_l_upstream_license_change_flagged(tmp)
    print("\nAll bootstrap/update tests passed.")


if __name__ == "__main__":
    main()
