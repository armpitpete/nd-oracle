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
        self.assertEqual("nd-singer-2016-date-representation-resolution", decision["id"])
        self.assertEqual("representation_decision_required", decision["status"])
        prohibited = set(decision["does_not_authorise"])
        self.assertIn("authoritative v0.1 mutation", prohibited)
        self.assertIn("authoritative v0.2 replacement", prohibited)
        self.assertIn("acceptance of 2016-07-03 as an exact publication fact", prohibited)
        self.assertIn("schema or validator change", prohibited)
        self.assertIn("ADHD migration or semantic disposition", prohibited)

    def test_exact_date_remains_candidate_not_accepted_fact(self) -> None:
        self.assertEqual("2016-07-03", self.research["candidate_date"])
        assessment = self.research["assessment"]
        self.assertEqual("moderate", assessment["day_level_evidence_strength"])
        self.assertFalse(assessment["day_level_candidate_usable_unqualified_in_v0_2_date"])
        self.assertFalse(assessment["ready_for_exact_date_acceptance"])
        self.assertFalse(assessment["automatic_verified_enrichment"])
        self.assertTrue(assessment["representation_problem_exposed"])
        self.assertIn("insufficient", assessment["reason"])
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

    def test_representation_analysis_preserves_three_routes(self) -> None:
        analysis = self.research["representation_analysis"]
        route_ids = [route["id"] for route in analysis["routes"]]
        self.assertEqual(
            [
                "stronger-asin-bound-evidence",
                "precision-aware-date-model",
                "retain-unmapped",
            ],
            route_ids,
        )
        self.assertEqual("precision-aware-date-model", analysis["preferred_research_direction"])
        self.assertFalse(analysis["authorises_schema_change"])
        self.assertIn("exact ISO date", analysis["current_v0_2_constraint"])

    def test_dostoevsky_check_preserves_reopening_routes(self) -> None:
        checks = self.research["dostoevsky_check"]["disconfirming_tests"]
        self.assertGreaterEqual(len(checks), 3)
        self.assertGreaterEqual(len(self.research["reopening_conditions"]), 4)
        self.assertIn("No conflict found", self.research["dostoevsky_check"]["result"])

    def test_proof_does_not_overstate_evidence_or_owner_authority(self) -> None:
        text = PROOF.read_text(encoding="utf-8")
        self.assertIn(
            "`2016-07-03` remains the best day-level candidate, but current evidence is insufficient to place it unqualified in the v0.2 `date` field.",
            text,
        )
        self.assertIn("Owner acceptance can decide how uncertainty is represented", text)
        self.assertIn("cannot convert uncertain metadata into a more certain fact", text)
        self.assertIn("precision-aware date representation", text)
        self.assertIn("Direct Amazon product metadata", text)
        self.assertIn("B01HY0QTEE", text)
        self.assertNotIn("Accept `2016-07-03` as the full publication date", text)


if __name__ == "__main__":
    unittest.main()
