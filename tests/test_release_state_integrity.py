from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
V12_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.2.md"
V11_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.1.md"
V10_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.0.md"

V12_RELEASE_SHA = "fad8e560979ba67bf94104d02f3b5100db8572cf"
V12_ARTIFACT_SHA256 = "b88c462115434d3ce9929f1e62ec29d0fb0095c13c05ec17c87b813afea426a1"
V12_DEPLOYMENT_RUN = "33490134037"
V12_VERIFICATION_RUN = "33490631672"
V11_RELEASE_SHA = "3032305dd81d48b2c6cc777b72f038267f995819"
V10_RELEASE_SHA = "a0081e7d879e23568792ad5a468250eeb21dd20b"


class ReleaseStateIntegrityTests(unittest.TestCase):
    def test_readme_names_accepted_v12_production(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("Production is the accepted v1.2 release", text)
        self.assertIn(V12_RELEASE_SHA, text)
        self.assertIn(V12_ARTIFACT_SHA256, text)
        self.assertIn("docs/PRODUCTION_STATE_v1.2.md", text)
        self.assertNotIn("Production is the accepted v1.1 bounded-discovery release", text)

    def test_v12_production_record_contains_exact_acceptance_evidence(self) -> None:
        text = V12_PRODUCTION.read_text(encoding="utf-8")
        for value in (
            V12_RELEASE_SHA,
            V12_ARTIFACT_SHA256,
            V12_DEPLOYMENT_RUN,
            V12_VERIFICATION_RUN,
        ):
            self.assertIn(value, text)
        self.assertIn("335-test permanent regression suite", text)
        self.assertIn("148 canonical", text)
        self.assertIn("125 authoritative objects", text)
        self.assertIn("600ea685.nd-oracle.pages.dev", text)

    def test_v11_production_evidence_remains_frozen(self) -> None:
        text = V11_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.1", text)
        self.assertIn(V11_RELEASE_SHA, text)
        self.assertIn("84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7", text)

    def test_v10_production_evidence_remains_frozen(self) -> None:
        text = V10_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.0", text)
        self.assertIn(V10_RELEASE_SHA, text)


if __name__ == "__main__":
    unittest.main()
