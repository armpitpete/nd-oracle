from __future__ import annotations

import dataclasses
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

from scripts import build_site, discovery


ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "contracts" / "current-production.json"
AUSTRALIA_EXTENSION = ROOT / "discovery" / "assessment-diagnosis-australia-v1.json"
CANADA_EXTENSION = ROOT / "discovery" / "assessment-diagnosis-canada-v1.json"
AUSTRALIA_BENCHMARK = ROOT / "benchmarks" / "assessment-diagnosis-australia-v1.json"
CANADA_BENCHMARK = ROOT / "benchmarks" / "assessment-diagnosis-canada-v1.json"
IRELAND_REVIEW = ROOT / "docs" / "IRELAND_POST_V1_READINESS_2026-09-05.md"
ARCH_REVIEW = ROOT / "docs" / "INTERNATIONAL_THREE_PACKAGE_ARCHITECTURE_REVIEW_v1.md"
AUSTRALIA_READINESS = ROOT / "docs" / "INTERNATIONAL_PILOT_AUSTRALIA_READINESS_v1.md"
AUSTRALIA_SOURCE_MATRIX = ROOT / "docs" / "ASSESSMENT_DIAGNOSIS_AUSTRALIA_SOURCE_MATRIX_v1.md"
CANADA_READINESS = ROOT / "docs" / "INTERNATIONAL_PILOT_CANADA_READINESS_v1.md"
CANADA_SOURCE_MATRIX = ROOT / "docs" / "ASSESSMENT_DIAGNOSIS_CANADA_SOURCE_MATRIX_v1.md"
BROWSER = ROOT / "scripts" / "discovery_browser.js"

BOOK_MEDIA_RESOURCES = {
    "were-all-neurodiverse",
    "caged-in-chaos",
    "front-of-the-class",
    "bbc-1800-seconds-on-autism",
    "inside-our-autistic-minds",
}
BOOK_MEDIA_QUESTIONS = {
    "neurodiversity-intro-media-where-start",
    "neurodivergent-book-accessible-formats",
    "neurodivergent-authorship-beyond-autism-adhd",
    "neurodiversity-podcast-documentary-how-check",
}
SLEEP_RESOURCES = {
    "nhs-inform-insomnia-scotland",
    "nhs-111-wales-insomnia",
    "nidirect-insomnia",
    "nhs-young-children-sleep",
}
SLEEP_QUESTIONS = {
    "insomnia-help-scotland",
    "insomnia-help-wales",
    "insomnia-help-northern-ireland",
    "child-sleep-where-start-uk",
}
FOOD_RESOURCES = {
    "nhs-inform-arfid-scotland",
    "nhs-111-wales-eating-disorders-arfid",
    "nhs-dysphagia",
    "nidirect-dysphagia",
}
FOOD_QUESTIONS = {
    "arfid-help-scotland",
    "arfid-help-wales",
    "swallowing-difficulty-food-safety",
    "child-restricted-eating-where-start",
}
MOBILITY_RESOURCES = {
    "govuk-bus-coach-disabled-help-gb",
    "govuk-bus-coach-accessible-information-gb",
    "orr-passenger-assistance-gb",
    "translink-accessibility-northern-ireland",
}
MOBILITY_QUESTIONS = {
    "bus-coach-assistance-great-britain",
    "rail-passenger-assistance-great-britain",
    "translink-assistance-northern-ireland",
    "travel-disruption-accessibility-planning",
}
INTERNATIONAL_RESOURCES = {
    "healthdirect-autism-australia",
    "healthdirect-adhd-australia",
    "canada-autism-assessment",
    "ontario-autism-assessment",
}
INTERNATIONAL_QUESTIONS = {
    "autism-assessment-australia",
    "adhd-assessment-australia",
    "autism-assessment-canada",
    "child-autism-assessment-ontario",
}
NEW_RESOURCES = (
    BOOK_MEDIA_RESOURCES
    | SLEEP_RESOURCES
    | FOOD_RESOURCES
    | MOBILITY_RESOURCES
    | INTERNATIONAL_RESOURCES
)
NEW_QUESTIONS = (
    BOOK_MEDIA_QUESTIONS
    | SLEEP_QUESTIONS
    | FOOD_QUESTIONS
    | MOBILITY_QUESTIONS
    | INTERNATIONAL_QUESTIONS
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pointer(document: object, path: str) -> object:
    current = document
    for raw in path.strip("/").split("/") if path else []:
        part = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list):
            current = current[int(part)]
        else:
            raise KeyError(path)
    return current


class ReferenceDepthInternationalCompletionV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = discovery.build_index()

    def test_exact_candidate_counts_and_public_route_contract(self) -> None:
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()

        self.assertEqual(20, len(concepts))
        self.assertEqual(168, len(resources))
        self.assertEqual(175, len(questions))
        self.assertEqual(3, len(evidence))
        self.assertEqual(366, len(concepts) + len(resources) + len(questions) + len(evidence))
        self.assertEqual(450, build_site.V10_ROUTE_COUNT)
        self.assertEqual(450, len(build_site.sitemap_paths(concepts, resources, questions)))

    def test_all_new_resources_are_reviewed_claimless_https_navigation(self) -> None:
        self.assertEqual(21, len(NEW_RESOURCES))
        for object_id in sorted(NEW_RESOURCES):
            item = load_json(ROOT / "objects" / "resources" / f"{object_id}.json")
            self.assertEqual("reviewed", item["status"], object_id)
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"], object_id)
            self.assertEqual("2026-09-05", item["provenance"]["last_reviewed"], object_id)
            self.assertEqual([], item["claims"], object_id)
            self.assertTrue(item["limitations"], object_id)
            urls = [x["value"] for x in item["locators"] if x["type"] == "url"]
            self.assertTrue(urls, object_id)
            self.assertTrue(all(x.startswith("https://") for x in urls), object_id)

    def test_new_questions_are_bounded_renderable_and_grouped_once(self) -> None:
        self.assertEqual(20, len(NEW_QUESTIONS))
        grouped = [object_id for _group, ids in build_site.QUESTION_GROUPS for object_id in ids]
        for object_id in sorted(NEW_QUESTIONS):
            item = load_json(ROOT / "objects" / "questions" / f"{object_id}.json")
            self.assertEqual("partially_resolved", item["status"], object_id)
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"], object_id)
            self.assertTrue(item["evidence_needed"], object_id)
            self.assertTrue(item["reopening_conditions"], object_id)
            self.assertEqual(1, grouped.count(object_id), object_id)
            for ref in item["related_objects"]:
                self.assertIn(ref["type"], {"concept", "resource"}, (object_id, ref))

    def test_books_media_breadth_and_non_clinical_authority_are_explicit(self) -> None:
        media = {
            object_id: load_json(ROOT / "objects" / "resources" / f"{object_id}.json")
            for object_id in BOOK_MEDIA_RESOURCES
        }
        self.assertEqual("media", media["bbc-1800-seconds-on-autism"]["category"])
        self.assertEqual("media", media["inside-our-autistic-minds"]["category"])
        self.assertIn(
            {"type": "concept", "id": "developmental-coordination-disorder"},
            media["caged-in-chaos"]["related_objects"],
        )
        self.assertIn(
            {"type": "concept", "id": "tourette-syndrome"},
            media["front-of-the-class"]["related_objects"],
        )
        formats = " ".join(media["were-all-neurodiverse"]["cost_or_access_notes"]).lower()
        self.assertIn("ebook", formats)
        self.assertIn("audiobook", formats)
        q = load_json(ROOT / "objects" / "questions" / "neurodiversity-podcast-documentary-how-check.json")
        self.assertIn("not", q["current_understanding"].lower())
        self.assertIn("clinical authority", q["current_understanding"].lower())

    def test_sleep_routes_preserve_diagnosis_and_medication_boundaries(self) -> None:
        for object_id in SLEEP_QUESTIONS:
            text = load_json(ROOT / "objects" / "questions" / f"{object_id}.json")["current_understanding"].lower()
            self.assertNotIn("you have insomnia", text, object_id)
        child = load_json(ROOT / "objects" / "questions" / "child-sleep-where-start-uk.json")
        child_text = child["current_understanding"].lower()
        self.assertIn("does not diagnose", child_text)
        self.assertIn("melatonin", child_text)
        existing = load_json(ROOT / "objects" / "questions" / "sleep-medication-melatonin-boundary.json")
        existing_text = existing["current_understanding"].lower()
        for action in ("start", "stop", "increase", "decrease"):
            self.assertIn(action, existing_text)

    def test_food_routes_separate_arfid_sensory_eating_and_swallowing_safety(self) -> None:
        swallow = load_json(ROOT / "objects" / "questions" / "swallowing-difficulty-food-safety.json")
        text = swallow["current_understanding"].lower()
        self.assertIn("swallowing problem", text)
        self.assertIn("dysphagia", text)
        self.assertIn("arfid", text)
        self.assertIn("sensory food preference", text)

        child = load_json(ROOT / "objects" / "questions" / "child-restricted-eating-where-start.json")
        child_text = child["current_understanding"].lower()
        self.assertIn("does not diagnose arfid", child_text)
        self.assertIn("swallowing", child_text)

    def test_mobility_layers_are_not_collapsed_into_provider_quality_or_one_uk_rule(self) -> None:
        translink = load_json(ROOT / "objects" / "resources" / "translink-accessibility-northern-ireland.json")
        self.assertIn("not an independent quality score", " ".join(translink["limitations"]).lower())
        gb = load_json(ROOT / "objects" / "resources" / "govuk-bus-coach-disabled-help-gb.json")
        self.assertIn("Northern Ireland", " ".join(gb["limitations"]))
        rail = load_json(ROOT / "objects" / "questions" / "rail-passenger-assistance-great-britain.json")
        self.assertIn("station", rail["current_understanding"].lower())
        self.assertIn("operator", rail["current_understanding"].lower())

    def test_ireland_deferred_work_is_resolved_as_an_evidence_decision_not_fake_coverage(self) -> None:
        text = IRELAND_REVIEW.read_text(encoding="utf-8")
        self.assertIn("child ADHD remains deliberately deferred", text)
        self.assertIn("do not activate another Ireland domain", text)
        self.assertIn("private-provider ranking", text)
        self.assertFalse((ROOT / "objects" / "questions" / "child-adhd-assessment-republic-ireland.json").exists())

    def test_australia_and_canada_scope_fingerprints_match_committed_objects(self) -> None:
        for extension_path in (AUSTRALIA_EXTENSION, CANADA_EXTENSION):
            extension = load_json(extension_path)
            for route, entry in extension["scope_provenance"]["routes"].items():
                parts = route.strip("/").split("/")
                source = ROOT / "objects" / parts[0] / f"{parts[1]}.json"
                document = load_json(source)
                value = pointer(document, entry["basis_path"])
                basis_sha = hashlib.sha256(canonical(value)).hexdigest()
                binding_sha = hashlib.sha256(
                    canonical({"basis_sha256": basis_sha, "scope": entry["scope"]})
                ).hexdigest()
                self.assertEqual(entry["basis_sha256"], basis_sha, route)
                self.assertEqual(entry["binding_sha256"], binding_sha, route)

    def test_final_jurisdiction_policy_is_additive_and_has_90_exact_scoped_routes(self) -> None:
        self.assertEqual(90, discovery.EXPECTED_SCOPED_ROUTE_COUNT)
        self.assertEqual(90, len(discovery.POLICY["scope_provenance"]["routes"]))
        self.assertEqual((["Australia"], False), discovery.requested_jurisdiction("assessment in Australia"))
        self.assertEqual((["Canada"], False), discovery.requested_jurisdiction("assessment in Canada"))
        self.assertEqual((["Canada", "Ontario"], False), discovery.requested_jurisdiction("assessment in Ontario"))

    def test_australia_and_canada_benchmarks_and_hostile_controls(self) -> None:
        for benchmark_path in (AUSTRALIA_BENCHMARK, CANADA_BENCHMARK):
            benchmark = load_json(benchmark_path)
            for case in benchmark["cases"]:
                trace, results = discovery.evaluate(case["query"], limit=10, index=self.index)
                self.assertTrue(results, case["query"])
                self.assertEqual(case["expected_top"], results[0].route, case["query"])
                expected_scope = set(discovery.POLICY["jurisdiction"]["scope_sets"][case["scope"]])
                self.assertEqual(expected_scope, set(discovery._route_scope(results[0].route) or []))
            for case in benchmark["hostile_controls"]:
                trace, results = discovery.evaluate(case["query"], limit=10, index=self.index)
                if "expected_final_reason" in case:
                    self.assertEqual(case["expected_final_reason"], trace["final_reason"], case["query"])
                    self.assertEqual([], results, case["query"])
                else:
                    actual = {item.route for item in results}
                    self.assertEqual(set(), actual & set(case["forbidden_routes"]), case["query"])

    def test_new_international_queries_have_python_browser_trace_parity(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required for browser decision-trace parity")
        queries = [
            "autism assessment Australia",
            "ADHD assessment Australia",
            "autism assessment Canada",
            "child autism assessment Ontario",
            "tell me whether I am autistic in Australia",
            "tell me whether my child is autistic in Ontario",
        ]
        payload = json.loads(discovery.browser_index_json())
        python_outputs = []
        for query in queries:
            trace, results = discovery.evaluate(query, limit=5, index=self.index)
            python_outputs.append({
                "trace": trace,
                "results": [dataclasses.asdict(item) for item in results],
            })
        completed = subprocess.run(
            [node, str(BROWSER)],
            input=json.dumps({"queries": queries, "payload": payload, "limit": 5}),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(python_outputs, json.loads(completed.stdout))

    def test_australia_and_canada_have_required_readiness_and_source_matrix_artifacts(self) -> None:
        for path in (
            AUSTRALIA_READINESS,
            AUSTRALIA_SOURCE_MATRIX,
            CANADA_READINESS,
            CANADA_SOURCE_MATRIX,
        ):
            self.assertTrue(path.is_file(), path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("2026-09-05", text)
        self.assertIn("PASS", AUSTRALIA_READINESS.read_text(encoding="utf-8"))
        self.assertIn("PASS", CANADA_READINESS.read_text(encoding="utf-8"))
        self.assertIn("state/territory", AUSTRALIA_SOURCE_MATRIX.read_text(encoding="utf-8"))
        self.assertIn("Federal/provincial", CANADA_SOURCE_MATRIX.read_text(encoding="utf-8"))

    def test_three_package_architecture_review_rejects_premature_schema_migration(self) -> None:
        text = ARCH_REVIEW.read_text(encoding="utf-8")
        self.assertIn("Retain additive jurisdiction sidecars", text)
        self.assertIn("Do not change the core object schema", text)
        self.assertIn("Do not begin mass-country expansion", text)

    def test_accepted_production_pointer_remains_frozen_until_protected_deployment(self) -> None:
        current = load_json(CURRENT)
        self.assertEqual("accepted", current["status"])
        self.assertEqual("94d1ab0d8df5699b1316e64d70c28fe11b25b7cf", current["source_sha"])
        self.assertEqual(325, current["corpus"]["governed_objects"])
        self.assertEqual(409, current["verification"]["canonical_routes_verified"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md",
            current["production_state_document"],
        )


if __name__ == "__main__":
    unittest.main()
