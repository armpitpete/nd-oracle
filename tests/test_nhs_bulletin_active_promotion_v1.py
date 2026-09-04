from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class NHSBulletinActivePromotionV1Tests(unittest.TestCase):
    def test_active_corpus_counts_and_routes(self) -> None:
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()
        self.assertEqual(20, len(concepts))
        self.assertEqual(146, len(resources))
        self.assertEqual(154, len(questions))
        self.assertEqual(3, len(evidence))
        self.assertEqual(323, len(concepts) + len(resources) + len(questions) + len(evidence))
        self.assertEqual(407, build_site.V10_ROUTE_COUNT)
        self.assertEqual(407, len(build_site.sitemap_paths(concepts, resources, questions)))

    def test_learning_disability_register_promotion_is_bounded(self) -> None:
        resource = load_json(ROOT / "objects" / "resources" / "nhs-england-learning-disability-register-and-health-checks.json")
        question = load_json(ROOT / "objects" / "questions" / "learning-disability-register-and-annual-health-check-england.json")
        self.assertEqual([], resource["claims"])
        self.assertTrue(any("not the same as a formal" in item.lower() for item in resource["limitations"]))
        text = question["current_understanding"].lower()
        self.assertIn("without requiring specialist confirmation", text)
        self.assertIn("not the same as a formal diagnosis", text)
        self.assertIn("does not establish eligibility for specialist", text)
        self.assertIn("aged 14+", text)

    def test_suicide_policy_promotion_cannot_become_crisis_authority(self) -> None:
        resource = load_json(ROOT / "objects" / "resources" / "nhs-england-staying-safe-from-suicide.json")
        question = load_json(ROOT / "objects" / "questions" / "person-centred-suicide-safety-policy-england.json")
        self.assertEqual([], resource["claims"])
        self.assertTrue(any("not an individual suicide-risk assessment" in item.lower() for item in resource["limitations"]))
        text = question["current_understanding"].lower()
        self.assertIn("static low, medium or high risk stratification", text)
        self.assertIn("collaborative personalised safety planning", text)
        self.assertIn("does not assess an individual's suicide risk", text)
        self.assertIn("urgent human services", text)

    def test_promotions_are_publicly_grouped(self) -> None:
        groups = {name: set(ids) for name, ids in build_site.QUESTION_GROUPS}
        self.assertIn("learning-disability-register-and-annual-health-check-england", groups["Healthcare access"])
        self.assertIn("person-centred-suicide-safety-policy-england", groups["Mental wellbeing"])

    def test_school_attendance_remains_candidate_until_exact_source_resolves(self) -> None:
        self.assertFalse((ROOT / "objects" / "resources" / "autism-central-school-attendance.json").exists())
        self.assertFalse((ROOT / "objects" / "questions" / "autistic-school-attendance-support-england.json").exists())
        self.assertTrue(
            (ROOT / "migration-candidates" / "post-baseline-nhs-bulletin-2026-09-04" / "resources" / "autism-central-school-attendance.json").exists()
        )
        self.assertTrue(
            (ROOT / "migration-candidates" / "post-baseline-nhs-bulletin-2026-09-04" / "questions" / "autistic-school-attendance-support-england.json").exists()
        )


if __name__ == "__main__":
    unittest.main()
