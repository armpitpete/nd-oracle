from __future__ import annotations

import subprocess
import sys
import unittest


class V12LiveAcceptanceProbeTests(unittest.TestCase):
    def test_ndoracle_org_matches_exact_main_contract(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/verify_live_site.py", "--origin", "https://ndoracle.org"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("V12_LIVE_ACCEPTANCE_OUTPUT_BEGIN")
        print(completed.stdout)
        print("V12_LIVE_ACCEPTANCE_OUTPUT_END")
        self.assertEqual(completed.returncode, 0, completed.stdout)


if __name__ == "__main__":
    unittest.main()
