from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
V11_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.1.md"
V10_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.0.md"

RELEASE_SHA = "3032305dd81d48b2c6cc777b72f038267f995819"
ARTIFACT_SHA256 = "84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7"
DEPLOYMENT_RUN = "33425750168"
VERIFICATION_RUN = "33426342672"


class ReleaseStateIntegrityTests(unittest.TestCase):
    def test_readme_names_accepted_v11_production(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("Production is the accepted v1.1 bounded-discovery release", text)
        self.assertIn(RELEASE_SHA, text)
        self.assertIn(ARTIFACT_SHA256, text)
        self.assertIn("docs/PRODUCTION_STATE_v1.1.md", text)
        self.assertNotIn("Production is the accepted v1.0 governed-discovery release", text)

    def test_v11_production_record_contains_exact_acceptance_evidence(self) -> None:
        text = V11_PRODUCTION.read_text(encoding="utf-8")
        for value in (RELEASE_SHA, ARTIFACT_SHA256, DEPLOYMENT_RUN, VERIFICATION_RUN):
            self.assertIn(value, text)
        self.assertIn("322-test regression suite", text)
        self.assertIn("142 canonical", text)
        self.assertIn("119 authoritative objects", text)

    def test_v10_production_evidence_remains_frozen(self) -> None:
        text = V10_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.0", text)
        self.assertIn("a0081e7d879e23568792ad5a468250eeb21dd20b", text)


if __name__ == "__main__":
    unittest.main()
