from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery


ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"

EXPECTED = {
    "Scotland": {
        "question": "/questions/disabled-student-support-scotland/",
        "resource": "/resources/saas-disabled-students-allowance/",
        "query": "disabled student support Scotland",
    },
    "Wales": {
        "question": "/questions/disabled-student-support-wales/",
        "resource": "/resources/student-finance-wales-disabled-students-allowance/",
        "query": "disabled student support Wales",
    },
    "Northern Ireland": {
        "question": "/questions/disabled-student-support-northern-ireland/",
        "resource": "/resources/northern-ireland-disabled-students-allowance/",
        "query": "disabled student support Northern Ireland",
    },
}


class V12NeedCoverageTests(unittest.TestCase):
    def test_expected_governed_object_counts(self) -> None:
        counts = {
            kind: len(list((OBJECTS / kind).glob("*.json")))
            for kind in ("concepts", "resources", "questions", "evidence")
        }
        self.assertEqual({"concepts": 20, "resources": 61, "questions": 41, "evidence": 3}, counts)
        self.assertEqual(125, sum(counts.values()))

    def test_each_new_nation_query_selects_matching_practical_question(self) -> None:
        for nation, expected in EXPECTED.items():
            with self.subTest(nation=nation):
                trace, results = discovery.evaluate(expected["query"], limit=10)
                self.assertEqual("results", trace["final_reason"])
                self.assertTrue(results)
                self.assertEqual(expected["question"], results[0].route)
                routes = {result.route for result in results}
                self.assertIn(expected["resource"], routes)

    def test_requested_jurisdiction_excludes_other_nations_scoped_routes(self) -> None:
        all_scoped = {
            value["question"] for value in EXPECTED.values()
        } | {
            value["resource"] for value in EXPECTED.values()
        } | {
            "/questions/disabled-student-support-england/",
            "/resources/disabled-students-allowance/",
        }
        for nation, expected in EXPECTED.items():
            with self.subTest(nation=nation):
                trace, results = discovery.evaluate(expected["query"], limit=20)
                routes = {result.route for result in results}
                allowed = {expected["question"], expected["resource"]}
                self.assertFalse((routes & all_scoped) - allowed)
                self.assertEqual([nation], trace["requested_scope"])

    def test_existing_england_student_support_route_remains_top(self) -> None:
        trace, results = discovery.evaluate("disabled student support England", limit=10)
        self.assertEqual("results", trace["final_reason"])
        self.assertTrue(results)
        self.assertEqual("/questions/disabled-student-support-england/", results[0].route)

    def test_personal_diagnosis_boundary_is_unchanged(self) -> None:
        trace, results = discovery.evaluate("I am in Scotland, am I autistic?")
        self.assertEqual([], results)
        self.assertEqual("clinical_diagnosis_boundary", trace["final_reason"])

    def test_new_resources_have_no_claim_authority(self) -> None:
        for object_id in (
            "saas-disabled-students-allowance",
            "student-finance-wales-disabled-students-allowance",
            "northern-ireland-disabled-students-allowance",
        ):
            with self.subTest(object_id=object_id):
                obj = json.loads((OBJECTS / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))
                self.assertEqual([], obj["claims"])
                self.assertEqual("reviewed", obj["status"])


if __name__ == "__main__":
    unittest.main()
