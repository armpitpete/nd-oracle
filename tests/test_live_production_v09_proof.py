from __future__ import annotations

import unittest

from scripts import verify_live_site


class LiveProductionV09ProofTests(unittest.TestCase):
    def test_live_production_matches_v09_contract(self) -> None:
        failures = verify_live_site.verify_production("https://ndoracle.org")
        self.assertEqual([], failures, "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
