from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "migration-candidates" / "autism-neurodiversity" / "evidence-date-precision-design.json"
PROOF = ROOT / "docs" / "migration-proofs" / "EVIDENCE_DATE_PRECISION_DESIGN.md"
CURRENT_EVIDENCE_SCHEMA = ROOT / "schema" / "types" / "evidence-v0.2.json"


class EvidenceDatePrecisionDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.design = json.loads(DESIGN.read_text(encoding="utf-8"))
        cls.current_schema = json.loads(CURRENT_EVIDENCE_SCHEMA.read_text(encoding="utf-8"))

    def test_design_is_non_authoritative_and_does_not_change_schema(self) -> None:
        self.assertFalse(self.design["authoritative"])
        self.assertFalse(self.design["schema_change_authorised"])
        self.assertEqual(
            "622da858f5803be32f409a54f7e0c6742f19e373",
            self.design["prepared_against_main"],
        )
        prohibited = set(self.design["decision_candidate"]["does_not_authorise"])
        self.assertIn("schema/types/evidence-v0.2.json mutation", prohibited)
        self.assertIn("validator change", prohibited)
        self.assertIn("acceptance of 2016-07-03 as an exact Singer publication fact", prohibited)
        self.assertIn("merge of PR 60", prohibited)

    def test_current_schema_problem_is_still_present_on_design_branch(self) -> None:
        properties = self.current_schema["properties"]
        self.assertIn("date", self.current_schema["required"])
        self.assertEqual("string", properties["date"]["type"])
        self.assertEqual("date", properties["date"]["format"])
        self.assertNotIn("date_precision", properties)

    def test_preferred_design_keeps_date_string_and_adds_explicit_precision(self) -> None:
        alternatives = {item["id"]: item for item in self.design["alternatives"]}
        self.assertEqual("preferred", alternatives["string-plus-explicit-precision"]["disposition"])
        contract = self.design["preferred_contract"]
        self.assertEqual("string", contract["date"]["type"])
        self.assertTrue(contract["date"]["required"])
        self.assertTrue(contract["date_precision"]["required"])
        self.assertEqual(["year", "month", "day"], contract["date_precision"]["enum"])
        self.assertFalse(contract["accessed_changes"])
        self.assertFalse(contract["date_confidence_field_proposed"])

    def test_singer_example_preserves_only_supported_precision(self) -> None:
        singer = self.design["singer_2016_example"]
        self.assertEqual("B01HY0QTEE", singer["asin"])
        self.assertEqual(
            {"date": "2016", "date_precision": "year"},
            singer["representation_if_design_implemented"],
        )
        self.assertEqual("2016-07-03", singer["day_level_candidate"])
        self.assertFalse(singer["day_level_candidate_goes_in_evidence_date"])

    def test_versioning_direction_is_bounded_to_pre_authoritative_v0_2_repair(self) -> None:
        versioning = self.design["versioning"]
        self.assertEqual(
            "repair-v0.2-in-place-before-authoritative-migration",
            versioning["preferred_direction"],
        )
        self.assertFalse(versioning["new_schema_version_proposed"])
        self.assertIn("authoritative knowledge remains v0.1", versioning["reason"])

    def test_future_validation_contract_contains_positive_and_negative_cases(self) -> None:
        tests = self.design["required_future_tests"]
        self.assertGreaterEqual(len(tests), 10)
        self.assertIn("year value with year precision validates", tests)
        self.assertIn("month value with month precision validates", tests)
        self.assertIn("full date with day precision validates", tests)
        self.assertIn("precision and value mismatches fail", tests)
        self.assertIn("invalid months fail", tests)
        self.assertIn("invalid full calendar dates fail", tests)
        self.assertIn("missing date_precision fails", tests)

    def test_proof_rejects_false_precision_and_exact_date_acceptance(self) -> None:
        text = PROOF.read_text(encoding="utf-8")
        self.assertIn("Never manufacture missing month/day components", text)
        self.assertIn('"date": "2016"', text)
        self.assertIn('"date_precision": "year"', text)
        self.assertIn("Precision is not confidence", text)
        self.assertIn("does not itself authorise", text)
        self.assertNotIn("Accept `2016-07-03` as the full publication date", text)


if __name__ == "__main__":
    unittest.main()
