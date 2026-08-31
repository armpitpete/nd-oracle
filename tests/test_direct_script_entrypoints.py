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
            result = subprocess.run([sys.executable, "scripts/build_site.py"], cwd=sandbox, text=True, capture_output=True, timeout=30)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("public site v1.0 candidate", result.stdout)
            for target in (
                sandbox / "dist" / "index.html",
                sandbox / "dist" / "questions" / "index.html",
                sandbox / "dist" / "books-media" / "index.html",
                sandbox / "dist" / "needs" / "index.html",
                sandbox / "dist" / "types" / "index.html",
                sandbox / "dist" / "places" / "index.html",
                sandbox / "dist" / "a-z" / "index.html",
                sandbox / "dist" / "find" / "index.html",
                sandbox / "dist" / "find.js",
                sandbox / "dist" / "questions" / "task-starting-and-organisation" / "index.html",
            ):
                self.assertTrue(target.is_file(), target)

    def test_live_verifier_runs_as_direct_script_before_network(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            sandbox = Path(tempdir)
            for name in ("scripts", "objects", "contracts"):
                shutil.copytree(ROOT / name, sandbox / name)
            result = subprocess.run([sys.executable, "scripts/verify_live_site.py", "--origin", "http://ndoracle.org"], cwd=sandbox, text=True, capture_output=True, timeout=30)
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertIn("Refusing non-HTTPS production origin.", result.stderr)


if __name__ == "__main__":
    unittest.main()
