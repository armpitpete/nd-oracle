from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "migration-candidates" / "post-baseline-nhs-bulletin-2026-09-04"
CURRENT = ROOT / "contracts" / "current-production.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PostBaselineNHSBulletinIngestV1Tests(unittest.TestCase):
    def test_ingest_boundary_remains_frozen_after_promotion_and_deployment(self) -> None:
        manifest = load_json(PACK / "manifest.json")
        current = load_json(CURRENT)
        frozen = manifest["frozen_production_boundary"]
        self.assertTrue(frozen["must_not_change_during_ingest"])
        self.assertEqual(319, frozen["governed_objects"])
        self.assertEqual(403, frozen["canonical_routes"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md",
            frozen["production_state_document"],
        )
        self.assertEqual(325, current["corpus"]["governed_objects"])
        self.assertEqual(409, current["verification"]["canonical_routes_verified"])
        self.assertGreater(current["corpus"]["governed_objects"], frozen["governed_objects"])
        self.assertGreater(current["verification"]["canonical_routes_verified"], frozen["canonical_routes"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md",
            current["production_state_document"],
        )
        self.assertNotEqual(frozen["production_state_document"], current["production_state_document"])

    def test_three_candidate_resources_are_claimless_and_reviewed(self) -> None:
        resource_dir = PACK / "resources"
        paths = sorted(resource_dir.glob("*.json"))
        self.assertEqual(3, len(paths))
        for path in paths:
            item = load_json(path)
            self.assertEqual("resource", item["type"])
            self.assertEqual("reviewed", item["status"])
            self.assertEqual([], item["claims"])
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"])
            self.assertTrue(item["locators"])
            self.assertTrue(item["limitations"])

    def test_three_candidate_questions_are_bounded(self) -> None:
        question_dir = PACK / "questions"
        paths = sorted(question_dir.glob("*.json"))
        self.assertEqual(3, len(paths))
        for path in paths:
            item = load_json(path)
            self.assertEqual("question", item["type"])
            self.assertEqual("partially_resolved", item["status"])
            self.assertTrue(item["related_objects"])
            self.assertTrue(item["evidence_needed"])
            self.assertTrue(item["reopening_conditions"])
            self.assertTrue(item["dissent"])

    def test_learning_disability_register_is_not_misrepresented_as_diagnosis(self) -> None:
        item = load_json(PACK / "questions" / "learning-disability-register-and-annual-health-check-england.json")
        text = item["current_understanding"].lower()
        self.assertIn("without requiring specialist confirmation", text)
        self.assertIn("not the same as a formal diagnosis", text)
        self.assertIn("does not establish eligibility for specialist", text)
        self.assertIn("aged 14+", text)

    def test_attendance_candidate_keeps_possible_causes_and_records_resolved_source(self) -> None:
        item = load_json(PACK / "questions" / "autistic-school-attendance-support-england.json")
        text = item["current_understanding"].lower()
        for phrase in ("anxiety", "sensory overwhelm", "bullying", "masking", "senco", "curiosity rather than blame"):
            self.assertIn(phrase, text)
        manifest = load_json(PACK / "manifest.json")
        self.assertEqual("promoted_production_accepted", manifest["status"])
        self.assertFalse(any("exact current Autism Central school-attendance destination" in gate for gate in manifest["promotion_gates"]))
        resolved = manifest["resolved_sources"]
        self.assertEqual(
            "https://www.autismcentral.nhs.uk/guidance/navigating-education",
            resolved["autism_central_education_hub"],
        )
        self.assertEqual(
            "https://www.autismcentral.nhs.uk/guidance/school-anxiety",
            resolved["autism_central_school_attendance"],
        )

    def test_suicide_policy_candidate_cannot_become_crisis_authority(self) -> None:
        item = load_json(PACK / "questions" / "person-centred-suicide-safety-policy-england.json")
        text = item["current_understanding"].lower()
        self.assertIn("static low, medium or high risk stratification", text)
        self.assertIn("collaborative personalised safety planning", text)
        self.assertIn("does not assess an individual's suicide risk", text)
        self.assertIn("does not", text)
        self.assertIn("urgent human services", text)


if __name__ == "__main__":
    unittest.main()
