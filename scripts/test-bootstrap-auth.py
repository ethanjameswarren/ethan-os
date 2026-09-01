#!/usr/bin/env python3
"""
Unit tests for the GitHub auth detection and publishing helpers introduced for
safe, resumable bootstrap publishing.

Run: python scripts/test-bootstrap-auth.py

These tests do not require a real GitHub account or network access. They mock
all subprocess and filesystem calls.
"""

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure the parent scripts directory is on the path for imports.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import github_auth

# Load publish-to-github.py as a module despite the hyphen in the filename.
spec = importlib.util.spec_from_file_location("publish_to_github", SCRIPTS_DIR / "publish-to-github.py")
publish_to_github = importlib.util.module_from_spec(spec)
sys.modules["publish_to_github"] = publish_to_github
spec.loader.exec_module(publish_to_github)


def fake_result(code=0, stdout="", stderr=""):
    r = MagicMock()
    r.returncode = code
    r.stdout = stdout
    r.stderr = stderr
    return r


class TestGithubAuth(unittest.TestCase):
    """Scenarios from the bootstrap auth audit."""

    @patch("github_auth.run")
    @patch("github_auth.shutil.which")
    def test_already_authenticated_via_gh_cli(self, which_mock, run_mock):
        which_mock.side_effect = lambda cmd: "/usr/bin/gh" if cmd == "gh" else "/usr/bin/git"
        run_mock.return_value = (0, "", "")
        state, message = github_auth.check_github_auth()
        self.assertEqual(state, github_auth.AuthState.AUTHENTICATED)
        self.assertIn("GitHub CLI is authenticated", message)

    @patch("github_auth.run")
    @patch("github_auth.shutil.which")
    def test_gh_cli_installed_but_not_logged_in(self, which_mock, run_mock):
        which_mock.side_effect = lambda cmd: "/usr/bin/gh" if cmd == "gh" else "/usr/bin/git"
        # Use a failing ssh return so the ssh fallback does not appear authenticated.
        run_mock.return_value = (255, "", "")
        state, _ = github_auth.check_github_auth()
        self.assertEqual(state, github_auth.AuthState.NEEDS_AUTH)

    @patch("github_auth.run")
    @patch("github_auth.shutil.which")
    def test_no_gh_but_ssh_works(self, which_mock, run_mock):
        which_mock.side_effect = lambda cmd: "/usr/bin/ssh" if cmd == "ssh" else "/usr/bin/git"

        def side_effect(cmd, cwd=None):
            if cmd[0] == "gh":
                return (127, "", "")
            # ssh exits 1 on successful github auth because GitHub closes the connection.
            return (1, "", "")

        run_mock.side_effect = side_effect
        state, message = github_auth.check_github_auth()
        self.assertEqual(state, github_auth.AuthState.AUTHENTICATED)
        self.assertIn("SSH", message)

    @patch("github_auth.run")
    @patch("github_auth.shutil.which")
    def test_no_gh_and_ssh_fails(self, which_mock, run_mock):
        which_mock.side_effect = lambda cmd: None

        def side_effect(cmd, cwd=None):
            if cmd[0] == "gh":
                return (127, "", "")
            return (255, "", "permission denied")

        run_mock.side_effect = side_effect
        state, _ = github_auth.check_github_auth()
        self.assertEqual(state, github_auth.AuthState.NEEDS_AUTH)

    @patch("github_auth.shutil.which")
    def test_git_not_installed(self, which_mock):
        which_mock.return_value = None
        state, message = github_auth.check_github_auth()
        self.assertEqual(state, github_auth.AuthState.NEEDS_AUTH)
        self.assertIn("Git is not installed", message)

    def test_beginner_recommendation_does_not_mention_token_or_password(self):
        text = github_auth.recommended_setup("beginner").lower()
        # "PAT" is only used as a warning word, not as a literal credential.
        self.assertNotIn("pat-in-url", text)
        self.assertNotIn("https://", text)  # no remote URL patterns at all
        self.assertNotIn("token", text)
        self.assertNotIn("password", text)
        self.assertIn("gh auth login", text)

    def test_advanced_recommendation_lists_secure_methods(self):
        text = github_auth.recommended_setup("advanced").lower()
        self.assertNotIn("pat-in-url", text)
        self.assertIn("ssh", text)
        self.assertIn("gh auth login", text)


class TestPublishToGithub(unittest.TestCase):
    """Publishing helper logic."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "caitlin-os"
        self.repo.mkdir()

    def _setup_git_remote_missing(self, subprocess_mock):
        """Make `subprocess.run` return a missing origin remote, then success for all others."""
        def side_effect(cmd, **kwargs):
            if "remote" in cmd and "get-url" in cmd:
                return fake_result(2, "", "fatal: No such remote")
            if "remote" in cmd and "add" in cmd:
                return fake_result(0, "", "")
            if "config" in cmd:
                return fake_result(0, "", "")
            return fake_result(0, "", "")

        subprocess_mock.side_effect = side_effect

    @patch("publish_to_github.subprocess.run")
    def test_set_origin_uses_https_without_token(self, subprocess_mock):
        self._setup_git_remote_missing(subprocess_mock)
        url = publish_to_github.set_origin(self.repo, "caitlin", "caitlin-os", use_ssh=False)
        self.assertEqual(url, "https://github.com/caitlin/caitlin-os.git")
        self.assertNotIn("@", url)  # No userinfo, no token
        self.assertNotIn(":", url.split("/")[-1])  # Not SSH, no port weirdness

    @patch("publish_to_github.subprocess.run")
    def test_set_origin_can_use_ssh(self, subprocess_mock):
        self._setup_git_remote_missing(subprocess_mock)
        url = publish_to_github.set_origin(self.repo, "caitlin", "caitlin-os", use_ssh=True)
        self.assertEqual(url, "git@github.com:caitlin/caitlin-os.git")

    @patch("shutil.which")
    @patch("publish_to_github.run_gh")
    def test_create_public_repo(self, run_gh_mock, which_mock):
        which_mock.return_value = "/usr/bin/gh"
        run_gh_mock.return_value = ""

        # Simulate repo does not exist by making gh repo view fail in repo_exists.
        with patch("publish_to_github.subprocess.run") as subprocess_mock:
            subprocess_mock.return_value = fake_result(1, "", "not found")
            created = publish_to_github.create_repo("caitlin", "caitlin-os", private=False)

        self.assertTrue(created)
        run_gh_mock.assert_called_once()
        args = run_gh_mock.call_args[0]
        self.assertIn("repo", args)
        self.assertIn("create", args)
        self.assertIn("--public", args)

    @patch("shutil.which")
    @patch("publish_to_github.run_gh")
    def test_create_private_companion_repo(self, run_gh_mock, which_mock):
        which_mock.return_value = "/usr/bin/gh"
        run_gh_mock.return_value = ""

        with patch("publish_to_github.subprocess.run") as subprocess_mock:
            subprocess_mock.return_value = fake_result(1, "", "not found")
            created = publish_to_github.create_repo("caitlin", "caitlin-life", private=True)

        self.assertTrue(created)
        args = run_gh_mock.call_args[0]
        self.assertIn("--private", args)

    @patch("shutil.which")
    @patch("publish_to_github.run_gh")
    def test_repo_exists_no_create(self, run_gh_mock, which_mock):
        which_mock.return_value = "/usr/bin/gh"

        # Simulate repo already exists on GitHub.
        with patch("publish_to_github.subprocess.run") as subprocess_mock:
            subprocess_mock.return_value = fake_result(0, "", "")
            created = publish_to_github.create_repo("caitlin", "caitlin-os", private=False)

        self.assertFalse(created)
        run_gh_mock.assert_not_called()

    @patch("publish_to_github.subprocess.run")
    def test_ensure_companion_creates_pointer_and_commit(self, subprocess_mock):
        subprocess_mock.return_value = fake_result(0, "", "")
        companion = Path(self.temp.name) / "caitlin-life"
        result = publish_to_github.ensure_companion(companion, "caitlin-os", Path("../caitlin-os"))
        pointer = result / ".caitlin-os-os.yaml"
        self.assertTrue(pointer.exists())
        self.assertIn("caitlin-os_os:", pointer.read_text(encoding="utf-8"))

    @patch("publish_to_github.check_github_auth")
    @patch("publish_to_github.publish_os")
    @patch("publish_to_github.publish_companion")
    @patch("publish_to_github.subprocess.run")
    def test_main_stops_and_is_resumable_when_not_authenticated(self, subprocess_mock, pub_comp_mock, pub_os_mock, auth_mock):
        auth_mock.return_value = (github_auth.AuthState.NEEDS_AUTH, "Not authenticated")
        with patch("sys.argv", ["publish-to-github.py", "--os-dir", str(self.repo), "--owner", "caitlin"]):
            code = publish_to_github.main()
        self.assertEqual(code, 1)
        pub_os_mock.assert_not_called()
        pub_comp_mock.assert_not_called()

    @patch("publish_to_github.check_github_auth")
    @patch("publish_to_github.publish_os")
    @patch("publish_to_github.publish_companion")
    @patch("publish_to_github.subprocess.run")
    def test_main_publishes_when_authenticated(self, subprocess_mock, pub_comp_mock, pub_os_mock, auth_mock):
        auth_mock.return_value = (github_auth.AuthState.AUTHENTICATED, "OK")
        with patch("sys.argv", ["publish-to-github.py", "--os-dir", str(self.repo), "--owner", "caitlin"]):
            code = publish_to_github.main()
        self.assertEqual(code, 0)
        pub_os_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
