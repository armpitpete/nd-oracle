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
        self.assertEqual(70, discovery.EXPECTED_SCOPED_ROUTE_COUNT)
        self.assertEqual(70, len(discovery.POLICY["scope_provenance"]["routes"]))
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
            if route_scope != expected_scope:
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

    def test_tampered_extension_scope_binding_is_rejected_by_policy_validation(self) -> None:
        route = sorted(self.extension["scope_provenance"]["routes"])[0]
        tampered = copy.deepcopy(discovery.POLICY)
        current = tampered["scope_provenance"]["routes"][route]["scope"]
        tampered["scope_provenance"]["routes"][route]["scope"] = "England" if current != "England" else "Scotland"
        with self.assertRaisesRegex(ValueError, "Scope declaration binding mismatch"):
            discovery.validate_policy(policy=tampered, index=self.index)


if __name__ == "__main__":
    unittest.main()
