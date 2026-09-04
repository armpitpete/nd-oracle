from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site, discovery

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "uk-breadth-v1.json"

NEW_QUESTION_IDS = (
    "appointments-admin-preparation",
    "arfid-information-without-self-diagnosis",
    "ask-service-email-text-instead-phone",
    "benefit-decision-disagree-which-process-uk",
    "budgeting-when-numbers-paperwork-hard",
    "children-young-people-neurodivergent-fiction",
    "choosing-neurodiversity-book-media",
    "clothing-touch-sensory-discomfort",
    "cooking-meal-preparation-executive-function",
    "coordination-mobility-travel-planning",
    "deadlines-renewals-appeals-remembering",
    "debt-missed-payments-where-start",
    "dental-appointment-sensory-anxiety-adjustments",
    "exams-assessment-adjustments-study",
    "find-local-neurodivergent-peer-group",
    "forms-official-paperwork-overwhelming",
    "get-help-with-money-admin-without-financial-advice",
    "hospital-appointment-reasonable-adjustments",
    "household-tasks-chore-overload",
    "letters-bills-correspondence-pile-up",
    "lived-experience-books-not-clinical-evidence",
    "low-mood-depression-where-start",
    "medication-information-without-changing-dose",
    "mental-health-appointments-communication-sensory-adjustments",
    "mixed-neurotype-communication-misunderstandings",
    "note-taking-and-lecture-access",
    "occupational-health-neurodivergent-what-to-expect",
    "online-peer-community-safety-fit",
    "operating-system-accessibility-settings",
    "parent-carer-peer-support-uk",
    "persistent-insomnia-when-seek-help",
    "public-transport-assistance-disabled-uk",
    "reduce-digital-distraction-and-motion",
    "restricted-food-range-when-seek-help",
    "school-college-transition-support-uk",
    "self-employed-disabled-work-support",
    "sensory-food-texture-smell-eating",
    "shift-work-sleep-routine",
    "sleep-environment-sensory-load",
    "sleep-medication-melatonin-boundary",
    "speech-to-text-and-voice-control",
    "staying-in-work-performance-process-adjustments",
    "talking-therapy-access-and-adjustments",
    "temperature-smell-taste-sensory-environment",
    "transitions-change-between-tasks",
    "trauma-distress-ptsd-assessment-boundary",
    "travel-sensory-overload-preparation",
    "urgent-mental-health-help-uk",
    "written-vs-spoken-communication-preference",
)

NEW_RESOURCE_IDS = (
    "acas-performance-and-adjustments",
    "adhd-uk-support-groups",
    "android-accessibility-features",
    "apple-iphone-cognitive-accessibility",
    "govuk-benefits-calculators",
    "govuk-disabled-transport-trains",
    "microsoft-windows-accessibility",
    "moneyhelper-budget-planner",
    "moneyhelper-debt-advice-locator",
    "nas-autism-eating-guide",
    "nas-autism-services-directory",
    "nas-autistic-adult-sleep-guide",
    "nas-mental-health-reasonable-adjustments",
    "nas-online-community",
    "nhs-balanced-diet-guidance",
    "nhs-eating-disorders-arfid",
    "nhs-england-reasonable-adjustment-digital-flag",
    "nhs-hospital-reasonable-adjustments",
    "nhs-insomnia",
    "nhs-scotland-therapy-information",
    "nhs-sleep-problems",
    "nhs-talking-therapies-england",
    "nidirect-access-to-work-ni",
    "uk-benefit-decision-challenge-signposts",
    "uk-school-transition-support-signposts",
    "uk-urgent-mental-health-help",
)


def load_question(object_id: str) -> dict:
    return json.loads((ROOT / "objects" / "questions" / f"{object_id}.json").read_text(encoding="utf-8"))


def load_resource(object_id: str) -> dict:
    return json.loads((ROOT / "objects" / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))


class UKBreadthV1Tests(unittest.TestCase):
    def test_candidate_corpus_and_route_contract(self) -> None:
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()
        self.assertGreaterEqual(len(concepts), 20)
        self.assertGreaterEqual(len(resources), 136)
        self.assertGreaterEqual(len(questions), 148)
        self.assertEqual(3, len(evidence))
        self.assertGreaterEqual(len(concepts) + len(resources) + len(questions) + len(evidence), 307)
        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, 391)
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(build_site.sitemap_paths(concepts, resources, questions)))

    def test_all_new_questions_are_bounded_reviewed_governed_routes(self) -> None:
        valid_statuses = {"partially_resolved", "not_currently_answerable"}
        self.assertEqual(49, len(NEW_QUESTION_IDS))
        for object_id in NEW_QUESTION_IDS:
            item = load_question(object_id)
            self.assertEqual(object_id, item["id"])
            self.assertIn(item["status"], valid_statuses, object_id)
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"], object_id)
            self.assertEqual("2026-09-03", item["provenance"]["last_reviewed"], object_id)
            self.assertTrue(item["why_it_matters"], object_id)
            self.assertTrue(item["related_objects"], object_id)
            self.assertTrue(item["evidence_needed"], object_id)
            self.assertTrue(item["reopening_conditions"], object_id)

    def test_all_new_resources_are_claimless_reviewed_https_routes(self) -> None:
        self.assertEqual(26, len(NEW_RESOURCE_IDS))
        for object_id in NEW_RESOURCE_IDS:
            item = load_resource(object_id)
            self.assertEqual(object_id, item["id"])
            self.assertEqual("reviewed", item["status"], object_id)
            self.assertEqual([], item["claims"], object_id)
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"], object_id)
            self.assertEqual("2026-09-03", item["provenance"]["last_reviewed"], object_id)
            self.assertTrue(item["locators"], object_id)
            self.assertTrue(
                all(locator["type"] == "url" and locator["value"].startswith("https://") for locator in item["locators"]),
                object_id,
            )
            self.assertTrue(item["limitations"], object_id)

    def test_uk_breadth_routes_are_publicly_projected(self) -> None:
        paths = set(build_site.sitemap_paths(build_site.load_concepts(), build_site.load_resources(), build_site.load_questions()))
        for object_id in NEW_QUESTION_IDS:
            self.assertIn(f"/questions/{object_id}/", paths, object_id)
        for object_id in NEW_RESOURCE_IDS:
            self.assertIn(f"/resources/{object_id}/", paths, object_id)

    def test_critical_clinical_and_crisis_boundaries_are_explicit(self) -> None:
        urgent = load_question("urgent-mental-health-help-uk")
        self.assertIn("does not perform suicide-risk assessment or crisis counselling", urgent["current_understanding"])
        urgent_resource = load_resource("uk-urgent-mental-health-help")
        self.assertTrue(any("emergency-service" in item for item in urgent_resource["limitations"]))

        arfid = load_question("arfid-information-without-self-diagnosis")
        self.assertIn("not a diagnosis", arfid["current_understanding"].lower())
        self.assertIn("assessment", arfid["current_understanding"].lower())

        sleep_med = load_question("sleep-medication-melatonin-boundary")
        sleep_text = sleep_med["current_understanding"].lower()
        for action in ("start", "stop", "increase", "decrease"):
            self.assertIn(action, sleep_text)
        self.assertIn("prescriber", sleep_text)

        medication = load_question("medication-information-without-changing-dose")
        med_text = medication["current_understanding"].lower()
        for action in ("start", "stop", "increase", "decrease"):
            self.assertIn(action, med_text)
        self.assertIn("prescriber", med_text)

        benefit = load_question("benefit-decision-disagree-which-process-uk")
        self.assertIn("cannot advise on legal grounds or prospects", benefit["current_understanding"].lower())

    def test_frozen_discovery_clinical_refusals_still_win(self) -> None:
        cases = (
            ("is my child autistic based on these signs", "clinical_diagnosis_boundary"),
            ("is my partner autistic", "clinical_diagnosis_boundary"),
            ("should I increase my ADHD medication dose", "clinical_medication_boundary"),
            ("should I stop my medicine because I feel better", "clinical_medication_boundary"),
        )
        for query, expected in cases:
            with self.subTest(query=query):
                trace, results = discovery.evaluate(query)
                self.assertEqual(expected, trace["final_reason"])
                self.assertEqual([], results)

    def test_29_case_discovery_and_hostile_benchmark(self) -> None:
        benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        self.assertEqual(29, len(benchmark["cases"]))
        for case in benchmark["cases"]:
            with self.subTest(query=case["query"]):
                trace, results = discovery.evaluate(case["query"], limit=5)
                if case["mode"] == "boundary":
                    self.assertEqual(case["expected_final_reason"], trace["final_reason"])
                    self.assertEqual([], results)
                    continue
                self.assertEqual("results", trace["final_reason"])
                routes = [result.route for result in results]
                rank = min(
                    (routes.index(route) + 1 for route in case["acceptable_routes"] if route in routes),
                    default=None,
                )
                self.assertIsNotNone(rank, f"{case['query']!r}: {routes}")
                self.assertLessEqual(rank, case["max_rank"], f"{case['query']!r}: {routes}")

    def test_accepted_production_truth_is_exact_verified_uk_baseline(self) -> None:
        current = json.loads((ROOT / "contracts" / "current-production.json").read_text(encoding="utf-8"))
        self.assertEqual("579c012cc9b31707409579da05b52a4d07efe61c", current["source_sha"])
        self.assertEqual(307, current["corpus"]["governed_objects"])
        self.assertEqual(391, current["verification"]["canonical_routes_verified"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md",
            current["production_state_document"],
        )

    def test_one_shot_writer_workflow_is_not_part_of_candidate(self) -> None:
        self.assertFalse((ROOT / ".github" / "workflows" / "uk-breadth-wire.yml").exists())

    def test_frozen_discovery_contract_remains_v11(self) -> None:
        policy = json.loads((ROOT / "discovery" / "routing-policy-v1.1.json").read_text(encoding="utf-8"))
        self.assertEqual("1.1", policy["version"])
        self.assertFalse(policy["orientation"]["enabled"])
        self.assertEqual(41, len(policy["scope_provenance"]["routes"]))


if __name__ == "__main__":
    unittest.main()
