from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-2016-full-date-research.json"
PROOF = ROOT / "docs" / "migration-proofs" / "SINGER_2016_FULL_DATE_RESEARCH.md"


class Singer2016FullDateResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.research = json.loads(RESEARCH.read_text(encoding="utf-8"))

    def test_research_is_non_authoritative_and_bounded(self) -> None:
        self.assertFalse(self.research["authoritative"])
        self.assertFalse(self.research["authoritative_replacement"])
        self.assertEqual(
            "622da858f5803be32f409a54f7e0c6742f19e373",
            self.research["prepared_against_main"],
        )
        decision = self.research["decision_candidate"]
        self.assertEqual("nd-singer-2016-full-date-resolution", decision["id"])
        self.assertEqual("owner_decision_required", decision["status"])
        prohibited = set(decision["does_not_authorise"])
        self.assertIn("authoritative v0.1 mutation", prohibited)
        self.assertIn("authoritative v0.2 replacement", prohibited)
        self.assertIn("ADHD migration or semantic disposition", prohibited)

    def test_exact_date_is_owner_review_candidate_not_auto_verified(self) -> None:
        self.assertEqual("2016-07-03", self.research["candidate_date"])
        assessment = self.research["assessment"]
        self.assertEqual("moderate", assessment["day_level_evidence_strength"])
        self.assertTrue(assessment["ready_for_owner_review"])
        self.assertFalse(assessment["automatic_verified_enrichment"])
        self.assertFalse(self.research["negative_and_limit_evidence"]["conflicting_day_level_date_found"])
        self.assertFalse(self.research["negative_and_limit_evidence"]["direct_amazon_product_metadata_retrieved"])

    def test_first_party_identity_and_secondary_day_are_kept_distinct(self) -> None:
        evidence = {item["id"]: item for item in self.research["evidence"]}
        self.assertEqual("first_party_author", evidence["singer-first-party-bibliography"]["source_class"])
        self.assertFalse(evidence["singer-first-party-bibliography"]["supports_exact_day"])
        self.assertEqual("secondary_bibliographic_metadata", evidence["goodreads-kindle-edition"]["source_class"])
        self.assertTrue(evidence["goodreads-kindle-edition"]["supports_exact_day"])
        self.assertFalse(evidence["singer-launch-post"]["supports_exact_day"])
        self.assertEqual("B01HY0QTEE", self.research["identity"]["asin"])

    def test_dostoevsky_check_preserves_reopening_routes(self) -> None:
        checks = self.research["dostoevsky_check"]["disconfirming_tests"]
        self.assertGreaterEqual(len(checks), 3)
        self.assertGreaterEqual(len(self.research["reopening_conditions"]), 3)
        self.assertIn("No conflict found", self.research["dostoevsky_check"]["result"])

    def test_proof_does_not_overstate_evidence(self) -> None:
        text = PROOF.read_text(encoding="utf-8")
        self.assertIn("owner review", text)
        self.assertIn("not", text.lower())
        self.assertIn("Direct Amazon product metadata", text)
        self.assertIn("2016-07-03", text)
        self.assertIn("B01HY0QTEE", text)


if __name__ == "__main__":
    unittest.main()
