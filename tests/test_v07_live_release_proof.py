from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V07LiveReleaseProofTests(unittest.TestCase):
    def test_exact_v07_verifier_accepts_canonical_production(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_live_site.py",
                "--origin",
                "https://ndoracle.org",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=90,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
