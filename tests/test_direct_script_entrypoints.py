from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DirectScriptEntrypointTests(unittest.TestCase):
    def test_build_site_runs_as_deployment_command(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            sandbox = Path(tempdir)
            for name in ("scripts", "objects", "site"):
                shutil.copytree(ROOT / name, sandbox / name)

            result = subprocess.run(
                [sys.executable, "scripts/build_site.py"],
                cwd=sandbox,
                text=True,
                capture_output=True,
                timeout=30,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("public site v0.7", result.stdout)
            self.assertTrue((sandbox / "dist" / "index.html").is_file())
            self.assertTrue((sandbox / "dist" / "questions" / "index.html").is_file())
            self.assertTrue(
                (
                    sandbox
                    / "dist"
                    / "questions"
                    / "task-starting-and-organisation"
                    / "index.html"
                ).is_file()
            )

    def test_live_verifier_runs_as_direct_script_before_network(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            sandbox = Path(tempdir)
            shutil.copytree(ROOT / "scripts", sandbox / "scripts")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_live_site.py",
                    "--origin",
                    "http://ndoracle.org",
                ],
                cwd=sandbox,
                text=True,
                capture_output=True,
                timeout=30,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("Refusing non-HTTPS production origin.", result.stderr)


if __name__ == "__main__":
    unittest.main()
