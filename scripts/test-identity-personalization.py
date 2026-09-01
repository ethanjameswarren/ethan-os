#!/usr/bin/env python3
"""
Tests for the identity / provenance separation introduced for Ethan OS.

Run: python scripts/test-identity-personalization.py
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure the parent scripts directory is on the path for imports.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from personalize import Personalizer, load_config


class TestIdentityPersonalization(unittest.TestCase):
    """Scenarios from the identity/provenance audit."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "john-os"
        self.repo.mkdir()

        (self.repo / "config").mkdir()
        (self.repo / "config" / "ethan-os.config.yaml").write_text(
            "framework:\n"
            "  id: ethan-os\n"
            "  name: Ethan OS\n"
            "  version: 0.1.1-beta\n"
            "identity:\n"
            "  owner_name: John\n"
            "  os_name: John OS\n"
            "  os_repo: john-os\n"
            "  life_repo: john-life\n",
            encoding="utf-8",
        )

        (self.repo / "LICENSE").write_text(
            "Copyright Ethan OS contributors\nApache 2.0\n", encoding="utf-8"
        )
        (self.repo / "NOTICE").write_text(
            "Ethan OS\nCopyright\n", encoding="utf-8"
        )
        (self.repo / ".os-upstream.yaml").write_text(
            "upstream:\n  project: Ethan OS\n  identifier: ethan-os\n",
            encoding="utf-8",
        )
        (self.repo / "README.md").write_text(
            "# Ethan OS\n\n"
            "Ethan OS helps Ethan manage personal state.\n\n"
            "[Ethan OS](https://github.com/ethanjameswarren/ethan-os.git) is the upstream framework.\n",
            encoding="utf-8",
        )

        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "capabilities").mkdir()
        (self.repo / "docs" / "capabilities" / "example.md").write_text(
            "# Example\n\nEthan OS helps Ethan organize his life.\n"
            "The companion repo is ethan-life, not ethan-os-life.\n",
            encoding="utf-8",
        )

        (self.repo / "workflows").mkdir()
        (self.repo / "workflows" / "core").mkdir()
        (self.repo / "workflows" / "core" / "update-from-upstream.md").write_text(
            "# Update from Ethan OS\n\nImport Ethan OS changes into Ethan OS.\n",
            encoding="utf-8",
        )

    def _run_personalizer(self):
        identity, framework = load_config(self.repo)
        return Personalizer(self.repo, identity, framework).personalize_repo()

    def test_protected_files_untouched(self):
        touched = self._run_personalizer()
        for name in ["LICENSE", "NOTICE", ".os-upstream.yaml", "config/ethan-os.config.yaml"]:
            self.assertNotIn(name, touched)
        self.assertIn("Ethan OS", (self.repo / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("Ethan OS", (self.repo / "NOTICE").read_text(encoding="utf-8"))
        self.assertIn("Ethan OS", (self.repo / ".os-upstream.yaml").read_text(encoding="utf-8"))

    def test_readme_title_and_body_personalized_attribution_preserved(self):
        self._run_personalizer()
        text = (self.repo / "README.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# John OS"))
        self.assertIn("John OS helps John manage personal state.", text)
        # Attribution link to the upstream framework must remain.
        self.assertIn("[Ethan OS](https://github.com/ethanjameswarren/ethan-os.git)", text)

    def test_user_facing_docs_personalized(self):
        touched = self._run_personalizer()
        self.assertIn("docs/capabilities/example.md", touched)
        text = (self.repo / "docs" / "capabilities" / "example.md").read_text(encoding="utf-8")
        self.assertIn("John OS helps John organize his life.", text)
        self.assertIn("companion repo is john-life", text)
        self.assertIn("not ethan-os-life", text)  # hyphenated compounds are not rewritten

    def test_core_workflows_protected(self):
        touched = self._run_personalizer()
        self.assertNotIn("workflows/core/update-from-upstream.md", touched)
        text = (self.repo / "workflows" / "core" / "update-from-upstream.md").read_text(encoding="utf-8")
        self.assertIn("Ethan OS", text)

    def test_config_identity_unchanged(self):
        self._run_personalizer()
        text = (self.repo / "config" / "ethan-os.config.yaml").read_text(encoding="utf-8")
        self.assertIn("id: ethan-os", text)
        self.assertIn("name: Ethan OS", text)
        self.assertIn("owner_name: John", text)
        self.assertIn("os_name: John OS", text)

    def test_idempotent(self):
        self._run_personalizer()
        second = self._run_personalizer()
        # After the first run, the second should have no additional changes.
        self.assertEqual(second, [])


if __name__ == "__main__":
    unittest.main()
