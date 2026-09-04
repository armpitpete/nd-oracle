from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
BASE_POLICY = ROOT / "discovery" / "routing-policy-v1.1.json"
EXTENSION = ROOT / "discovery" / "assessment-diagnosis-uk-v1.json"
BENCHMARK = ROOT / "benchmarks" / "assessment-diagnosis-uk-v1.json"
NATIONS = ("England", "Scotland", "Wales", "Northern Ireland")
ASSESSMENT_RESOURCE_IDS = (
    "betsi-cadwaladr-child-neurodevelopmental-assessment",
    "cardiff-vale-adult-autism-assessment",
    "dhcw-child-neurodevelopmental-assessments-wales",
    "health-ni-adhd-needs-assessment-2026",
    "hywel-dda-adult-adhd",
    "nhs-adhd-children-young-people",
    "nhs-england-autism-assessments",
    "nhs-inform-adhd-adults-scotland",
    "nhs-inform-adhd-children-scotland",
    "nhs-inform-autism-adults-scotland",
    "nhs-inform-autism-children-scotland",
    "nice-autism-under-19s-guideline",
    "nidirect-autism-assessment-northern-ireland",
    "northern-trust-paediatric-adhd-assessment",
    "welsh-government-neurodivergence-improvement-2026-27",
)


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


class AssessmentDiagnosisUKV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(BASE_POLICY.read_text(encoding="utf-8"))
        cls.extension = json.loads(EXTENSION.read_text(encoding="utf-8"))
        cls.benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        cls.index = discovery.build_index()

    def test_extension_is_additive_and_exactly_29_routes(self) -> None:
        base_routes = self.base["scope_provenance"]["routes"]
        extension_routes = self.extension["scope_provenance"]["routes"]
        self.assertEqual(41, len(base_routes))
        self.assertEqual(29, len(extension_routes))
        self.assertEqual(set(), set(base_routes) & set(extension_routes))
        self.assertEqual(70, len(base_routes) + len(extension_routes))
        self.assertEqual(82, discovery.EXPECTED_SCOPED_ROUTE_COUNT)
        self.assertEqual(82, len(discovery.POLICY["scope_provenance"]["routes"]))
        self.assertEqual(set(), set(self.base["intent_phrases"]) & set(self.extension["intent_phrases"]))
        discovery.validate_policy(index=self.index)

    def test_all_29_extension_fingerprints_match_committed_governed_objects(self) -> None:
        failures = []
        for route, entry in sorted(self.extension["scope_provenance"]["routes"].items()):
            parts = route.strip("/").split("/")
            source = ROOT / "objects" / parts[0] / f"{parts[1]}.json"
            if not source.is_file():
                failures.append((route, "missing source"))
                continue
            document = json.loads(source.read_text(encoding="utf-8"))
            value = pointer(document, entry["basis_path"])
            basis_sha = hashlib.sha256(canonical(value)).hexdigest()
            binding_sha = hashlib.sha256(canonical({"basis_sha256": basis_sha, "scope": entry["scope"]})).hexdigest()
            if basis_sha != entry["basis_sha256"]:
                failures.append((route, "basis", basis_sha, entry["basis_sha256"]))
            if binding_sha != entry["binding_sha256"]:
                failures.append((route, "binding", binding_sha, entry["binding_sha256"]))
        self.assertEqual([], failures)

    def test_benchmark_routes_to_expected_question_and_scope(self) -> None:
        failures = []
        scope_sets = discovery.POLICY["jurisdiction"]["scope_sets"]
        for case in self.benchmark["cases"]:
            trace, results = discovery.evaluate(case["query"], limit=5, index=self.index)
            top = results[0].route if results else None
            if top != case["expected_top"]:
                failures.append((case["query"], top, case["expected_top"], trace["final_reason"]))
                continue
            route_scope = set(discovery._route_scope(top) or [])
            expected_scope = set(scope_sets[case["scope"]])
            if case["scope"] == "United Kingdom":
                if route_scope:
                    failures.append((case["query"], "unexpected route scope", sorted(route_scope)))
                if set(trace["requested_scope"]) != expected_scope:
                    failures.append((case["query"], "requested scope", sorted(trace["requested_scope"]), sorted(expected_scope)))
            elif route_scope != expected_scope:
                failures.append((case["query"], "scope", sorted(route_scope), sorted(expected_scope)))
        self.assertEqual([], failures)

    def test_hostile_jurisdiction_and_clinical_controls(self) -> None:
        failures = []
        for case in self.benchmark["hostile_controls"]:
            trace, results = discovery.evaluate(case["query"], limit=10, index=self.index)
            if "expected_final_reason" in case:
                if trace["final_reason"] != case["expected_final_reason"] or results:
                    failures.append((case["query"], trace["final_reason"], [item.route for item in results]))
                continue
            actual = {item.route for item in results}
            leaked = sorted(actual & set(case["forbidden_routes"]))
            if leaked:
                failures.append((case["query"], "incompatible routes leaked", leaked))
        self.assertEqual([], failures)

    def test_indirect_child_diagnosis_requests_fail_closed(self) -> None:
        for query in (
            "can you tell me whether my child has ADHD?",
            "can you tell me whether my child is autistic?",
            "could you confirm if my son has autism?",
        ):
            with self.subTest(query=query):
                trace, results = discovery.evaluate(query, limit=10, index=self.index)
                self.assertEqual("clinical_diagnosis_boundary", trace["final_reason"])
                self.assertEqual([], results)

    def test_every_new_nation_question_fails_closed_in_incompatible_nations(self) -> None:
        scope_sets = discovery.POLICY["jurisdiction"]["scope_sets"]
        failures = []
        for route, entry in sorted(self.extension["scope_provenance"]["routes"].items()):
            if not route.startswith("/questions/") or entry["scope"] not in NATIONS:
                continue
            intent = self.extension["intent_phrases"].get(route, [None])[0]
            if not intent:
                failures.append((route, "missing intent"))
                continue
            allowed = set(scope_sets[entry["scope"]])
            for nation in NATIONS:
                if nation in allowed:
                    continue
                query = f"{intent} {nation}"
                trace, results = discovery.evaluate(query, limit=10, index=self.index)
                if route in trace["survivors"] or route in {item.route for item in results}:
                    failures.append((route, nation, trace["final_reason"]))
        self.assertEqual([], failures)

    def test_assessment_questions_use_publicly_renderable_related_types(self) -> None:
        failures = []
        routes = {case["expected_top"] for case in self.benchmark["cases"] if case["expected_top"].startswith("/questions/")}
        for route in sorted(routes):
            question_id = route.strip("/").split("/")[1]
            document = json.loads((ROOT / "objects" / "questions" / f"{question_id}.json").read_text(encoding="utf-8"))
            unsupported = sorted({item["type"] for item in document["related_objects"]} - {"concept", "resource"})
            if unsupported:
                failures.append((route, unsupported))
        self.assertEqual([], failures)

    def test_new_assessment_resources_remain_reviewed_claimless_navigation_records(self) -> None:
        failures = []
        for resource_id in ASSESSMENT_RESOURCE_IDS:
            document = json.loads((ROOT / "objects" / "resources" / f"{resource_id}.json").read_text(encoding="utf-8"))
            if document["status"] != "reviewed":
                failures.append((resource_id, "status", document["status"]))
            if document["claims"] != []:
                failures.append((resource_id, "claims", document["claims"]))
            if not document["locators"] or not all(locator["value"].startswith("https://") for locator in document["locators"] if locator["type"] == "url"):
                failures.append((resource_id, "locators"))
        self.assertEqual([], failures)

    def test_england_right_to_choose_does_not_leak_into_other_nations(self) -> None:
        england_routes = {
            "/questions/adult-autism-assessment-england/",
            "/questions/adult-adhd-assessment-england/",
        }
        failures = []
        for query in (
            "Right to Choose adult autism assessment Scotland",
            "Right to Choose adult ADHD assessment Wales",
            "Right to Choose adult autism assessment Northern Ireland",
        ):
            trace, results = discovery.evaluate(query, limit=10, index=self.index)
            leaked = sorted(england_routes & {item.route for item in results})
            if leaked:
                failures.append((query, trace["requested_scope"], leaked))
        self.assertEqual([], failures)

    def test_tampered_extension_scope_binding_is_rejected_by_policy_validation(self) -> None:
        route = sorted(self.extension["scope_provenance"]["routes"])[0]
        tampered = copy.deepcopy(discovery.POLICY)
        current = tampered["scope_provenance"]["routes"][route]["scope"]
        tampered["scope_provenance"]["routes"][route]["scope"] = "England" if current != "England" else "Scotland"
        with self.assertRaisesRegex(ValueError, "Scope declaration binding mismatch"):
            discovery.validate_policy(policy=tampered, index=self.index)


if __name__ == "__main__":
    unittest.main()
