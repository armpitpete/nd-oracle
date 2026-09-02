from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery


ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"

EXPECTED = {
    "Scotland": {
        "question": "/questions/healthcare-communication-adjustments-scotland/",
        "resource": "/resources/nhs-scotland-healthcare-communication-support/",
        "queries": (
            "healthcare communication adjustments Scotland",
            "communication adjustments healthcare Scotland",
            "reasonable communication adjustments NHS Scotland",
        ),
    },
    "Wales": {
        "question": "/questions/healthcare-communication-adjustments-wales/",
        "resource": "/resources/nhs-wales-accessible-communication-standards/",
        "queries": (
            "healthcare communication adjustments Wales",
            "communication adjustments healthcare Wales",
            "accessible communication health appointment Wales",
        ),
    },
    "Northern Ireland": {
        "question": "/questions/healthcare-communication-adjustments-northern-ireland/",
        "resource": "/resources/northern-ireland-healthcare-communication-access/",
        "queries": (
            "healthcare communication adjustments Northern Ireland",
            "communication adjustments healthcare Northern Ireland",
            "longer GP appointment communication Northern Ireland",
        ),
    },
}


class V12HealthcareParityTests(unittest.TestCase):
    def test_current_governed_object_counts(self) -> None:
        counts = {
            kind: len(list((OBJECTS / kind).glob("*.json")))
            for kind in ("concepts", "resources", "questions", "evidence")
        }
        self.assertEqual({"concepts": 20, "resources": 76, "questions": 55, "evidence": 3}, counts)
        self.assertEqual(154, sum(counts.values()))

    def test_each_nation_query_selects_matching_question_and_resource(self) -> None:
        for nation, expected in EXPECTED.items():
            for query in expected["queries"]:
                with self.subTest(nation=nation, query=query):
                    trace, results = discovery.evaluate(query, limit=20)
                    self.assertEqual("results", trace["final_reason"])
                    self.assertEqual([nation], trace["requested_scope"])
                    self.assertTrue(results)
                    self.assertEqual(expected["question"], results[0].route)
                    self.assertIn(expected["resource"], {result.route for result in results})

    def test_requested_jurisdiction_excludes_other_healthcare_nations(self) -> None:
        healthcare_routes = {
            value["question"] for value in EXPECTED.values()
        } | {
            value["resource"] for value in EXPECTED.values()
        } | {
            "/questions/healthcare-communication-adjustments-england/",
            "/resources/nhs-england-accessible-information-adjustments/",
        }
        for nation, expected in EXPECTED.items():
            with self.subTest(nation=nation):
                trace, results = discovery.evaluate(expected["queries"][0], limit=30)
                routes = {result.route for result in results}
                allowed = {expected["question"], expected["resource"]}
                self.assertFalse((routes & healthcare_routes) - allowed)
                self.assertEqual([nation], trace["requested_scope"])

    def test_existing_england_healthcare_route_remains_top(self) -> None:
        trace, results = discovery.evaluate("healthcare communication adjustments England", limit=20)
        self.assertEqual("results", trace["final_reason"])
        self.assertEqual(["England"], trace["requested_scope"])
        self.assertTrue(results)
        self.assertEqual("/questions/healthcare-communication-adjustments-england/", results[0].route)
        self.assertIn(
            "/resources/nhs-england-accessible-information-adjustments/",
            {result.route for result in results},
        )

    def test_new_resources_are_reviewed_non_claim_bearing_navigation_records(self) -> None:
        for object_id in (
            "nhs-scotland-healthcare-communication-support",
            "nhs-wales-accessible-communication-standards",
            "northern-ireland-healthcare-communication-access",
        ):
            with self.subTest(object_id=object_id):
                obj = json.loads((OBJECTS / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))
                self.assertEqual("reviewed", obj["status"])
                self.assertEqual([], obj["claims"])
                self.assertTrue(obj["locators"])
                self.assertTrue(all(locator["value"].startswith("https://") for locator in obj["locators"]))

    def test_scotland_learning_disability_source_is_explicitly_audience_limited(self) -> None:
        obj = json.loads((OBJECTS / "resources" / "nhs-scotland-healthcare-communication-support.json").read_text(encoding="utf-8"))
        text = " ".join([obj["audience_or_context"], *obj["limitations"]]).lower()
        self.assertIn("specifically", text)
        self.assertIn("learning disability", text)
        self.assertIn("not", text)
        self.assertIn("general", text)

    def test_northern_ireland_does_not_import_equality_act_framing(self) -> None:
        paths = (
            OBJECTS / "questions" / "healthcare-communication-adjustments-northern-ireland.json",
            OBJECTS / "resources" / "northern-ireland-healthcare-communication-access.json",
        )
        for path in paths:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("Equality Act 2010 applies", text)
                self.assertIn("Northern Ireland", text)

    def test_clinical_boundary_and_orientation_are_unchanged(self) -> None:
        trace, results = discovery.evaluate("I am in Wales, am I autistic?")
        self.assertEqual([], results)
        self.assertEqual("clinical_diagnosis_boundary", trace["final_reason"])
        trace, results = discovery.evaluate("Should I increase my ADHD medication in Scotland?")
        self.assertEqual([], results)
        self.assertEqual("clinical_medication_boundary", trace["final_reason"])
        self.assertFalse(discovery.POLICY["orientation"]["enabled"])
        self.assertEqual(
            {
                "identity_bonus": 160,
                "routing_phrase_bonus": 130,
                "title_exact_bonus": 120,
                "title_contains_bonus": 55,
                "body_contains_bonus": 20,
                "identity_token_weight": 14,
                "body_token_weight": 3,
                "intent_full_bonus": 70,
                "intent_token_weight": 8,
            },
            discovery.POLICY["ranking"],
        )

    def test_six_new_routes_have_exact_scope_provenance(self) -> None:
        entries = discovery.POLICY["scope_provenance"]["routes"]
        for nation, expected in EXPECTED.items():
            with self.subTest(nation=nation):
                self.assertEqual(nation, entries[expected["question"]]["scope"])
                self.assertEqual("/question", entries[expected["question"]]["basis_path"])
                self.assertEqual(nation, entries[expected["resource"]]["scope"])
                self.assertEqual("/audience_or_context", entries[expected["resource"]]["basis_path"])


if __name__ == "__main__":
    unittest.main()
