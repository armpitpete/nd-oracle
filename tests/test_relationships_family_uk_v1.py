from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "relationships-family-uk-v1.json"

NEW_RESOURCE_IDS = (
    "nas-making-friends-autistic-adults",
    "nas-family-relationships",
    "nhs-supporting-autistic-child",
    "contact-parent-carer-helpline-uk",
    "govuk-domestic-abuse-help",
    "uk-consent-healthy-relationships-starting-points",
    "uk-disability-service-access-starting-points",
    "leicestershire-nhs-autism-communication-support",
)

NEW_QUESTION_IDS = (
    "friendship-misunderstandings-neurodivergent",
    "partner-communication-processing-sensory-needs",
    "boundaries-neurodivergent-relationships",
    "conflict-repair-processing-time-relationships",
    "intimacy-consent-sensory-communication",
    "parenting-neurodivergent-child-uk",
    "disabled-neurodivergent-parent-service-access-uk",
    "family-events-sensory-social-load",
    "relationship-safety-domestic-abuse-help",
    "should-i-leave-or-stay-relationship-boundary",
)


class RelationshipsFamilyUKV1Tests(unittest.TestCase):
    def test_new_resources_are_claimless_reviewed_https_routes(self) -> None:
        for object_id in NEW_RESOURCE_IDS:
            item = json.loads((ROOT / "objects" / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))
            self.assertEqual(item["status"], "reviewed", object_id)
            self.assertEqual(item["claims"], [], object_id)
            self.assertTrue(item["locators"], object_id)
            self.assertTrue(all(locator["type"] == "url" and locator["value"].startswith("https://") for locator in item["locators"]), object_id)
            self.assertEqual(item["provenance"]["last_reviewed"], "2026-09-03", object_id)
            self.assertTrue(item["limitations"], object_id)

    def test_new_questions_preserve_bounded_status_and_references(self) -> None:
        valid_statuses = {"partially_resolved", "not_currently_answerable"}
        for object_id in NEW_QUESTION_IDS:
            item = json.loads((ROOT / "objects" / "questions" / f"{object_id}.json").read_text(encoding="utf-8"))
            self.assertIn(item["status"], valid_statuses, object_id)
            self.assertTrue(item["related_objects"], object_id)
            self.assertTrue(item["evidence_needed"], object_id)
            self.assertTrue(item["reopening_conditions"], object_id)

    def test_parent_and_parenting_child_are_distinct_journeys(self) -> None:
        trace, results = discovery.evaluate("support parenting a neurodivergent child UK")
        self.assertEqual(trace["final_reason"], "results")
        self.assertTrue(results)
        self.assertEqual(results[0].route, "/questions/parenting-neurodivergent-child-uk/")
        self.assertNotEqual(results[0].route, "/questions/autistic-parent-support-uk/")

    def test_friendship_baseline_no_match_is_repaired(self) -> None:
        trace, results = discovery.evaluate("friendship misunderstandings autism")
        self.assertEqual(trace["final_reason"], "results")
        self.assertTrue(results)
        self.assertEqual(results[0].route, "/questions/friendship-misunderstandings-neurodivergent/")

    def test_safeguarding_is_not_only_ordinary_relationship_communication(self) -> None:
        trace, results = discovery.evaluate("partner controlling me domestic abuse help")
        self.assertEqual(trace["final_reason"], "results")
        self.assertTrue(results)
        self.assertEqual(results[0].route, "/questions/relationship-safety-domestic-abuse-help/")
        self.assertNotEqual(results[0].route, "/questions/communication-needs-in-relationships/")

    def test_existing_clinical_boundaries_remain_authoritative(self) -> None:
        trace, results = discovery.evaluate("is my partner autistic")
        self.assertEqual(trace["final_reason"], "clinical_diagnosis_boundary")
        self.assertEqual(results, [])
        trace, results = discovery.evaluate("should I increase my ADHD medication because relationship stress")
        self.assertEqual(trace["final_reason"], "clinical_medication_boundary")
        self.assertEqual(results, [])

    def test_disability_access_resource_preserves_uk_legal_split(self) -> None:
        item = json.loads((ROOT / "objects" / "resources" / "uk-disability-service-access-starting-points.json").read_text(encoding="utf-8"))
        self.assertIn("England, Scotland and Wales", item["audience_or_context"])
        self.assertIn("Northern Ireland", item["audience_or_context"])
        urls = {locator["value"] for locator in item["locators"]}
        self.assertTrue(any("equalityhumanrights.com" in url for url in urls))
        self.assertTrue(any("equalityni.org" in url for url in urls))
        self.assertTrue(any("not legal advice" in limit.lower() for limit in item["limitations"]))

    def test_48_case_benchmark(self) -> None:
        benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        self.assertEqual(len(benchmark["cases"]), 48)
        for case in benchmark["cases"]:
            with self.subTest(query=case["query"]):
                trace, results = discovery.evaluate(case["query"], limit=5)
                if case["mode"] == "boundary":
                    self.assertEqual(trace["final_reason"], case["expected_final_reason"])
                    self.assertEqual(results, [])
                    continue
                self.assertEqual(trace["final_reason"], "results")
                routes = [result.route for result in results]
                rank = min((routes.index(route) + 1 for route in case["acceptable_routes"] if route in routes), default=None)
                self.assertIsNotNone(rank, f"{case['query']!r}: {routes}")
                self.assertLessEqual(rank, case["max_rank"], f"{case['query']!r}: {routes}")


if __name__ == "__main__":
    unittest.main()
