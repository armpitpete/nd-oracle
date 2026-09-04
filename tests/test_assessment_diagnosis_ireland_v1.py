from __future__ import annotations

import dataclasses
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

from scripts import discovery


ROOT = Path(__file__).resolve().parents[1]
BASE_POLICY = ROOT / "discovery" / "routing-policy-v1.1.json"
UK_EXTENSION = ROOT / "discovery" / "assessment-diagnosis-uk-v1.json"
IRELAND_EXTENSION = ROOT / "discovery" / "assessment-diagnosis-ireland-v1.json"
BENCHMARK = ROOT / "benchmarks" / "assessment-diagnosis-ireland-v1.json"
CURRENT_PRODUCTION = ROOT / "contracts" / "current-production.json"
BROWSER = ROOT / "scripts" / "discovery_browser.js"

IRELAND_RESOURCE_IDS = (
    "hse-autism-assessment-republic-ireland",
    "hse-autism-assessment-process-republic-ireland",
    "hse-autism-protocol-2026-republic-ireland",
    "hse-adult-adhd-model-care-republic-ireland",
    "hse-adult-adhd-team-status-2026-republic-ireland",
    "hse-childrens-disability-referral-republic-ireland",
    "hse-assessment-of-need-republic-ireland",
    "hse-health-regions-republic-ireland",
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


class AssessmentDiagnosisIrelandV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(BASE_POLICY.read_text(encoding="utf-8"))
        cls.uk_extension = json.loads(UK_EXTENSION.read_text(encoding="utf-8"))
        cls.extension = json.loads(IRELAND_EXTENSION.read_text(encoding="utf-8"))
        cls.benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        cls.index = discovery.build_index()

    def test_exact_candidate_corpus_and_route_contract(self) -> None:
        from scripts import build_site

        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()

        self.assertEqual(20, len(concepts))
        self.assertGreaterEqual(len(resources), 144)
        self.assertGreaterEqual(len(questions), 152)
        self.assertEqual(3, len(evidence))
        self.assertGreaterEqual(len(concepts) + len(resources) + len(questions) + len(evidence), 319)
        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, 403)
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(build_site.sitemap_paths(concepts, resources, questions)))

    def test_extension_is_additive_after_frozen_uk_scope_state(self) -> None:
        base_routes = self.base["scope_provenance"]["routes"]
        uk_routes = self.uk_extension["scope_provenance"]["routes"]
        ireland_routes = self.extension["scope_provenance"]["routes"]

        self.assertEqual(41, len(base_routes))
        self.assertEqual(29, len(uk_routes))
        self.assertEqual(12, len(ireland_routes))
        self.assertEqual(70, self.extension["base_scope_count"])
        self.assertEqual(set(), set(base_routes) & set(ireland_routes))
        self.assertEqual(set(), set(uk_routes) & set(ireland_routes))
        self.assertEqual(82, discovery.EXPECTED_SCOPED_ROUTE_COUNT)
        self.assertEqual(82, len(discovery.POLICY["scope_provenance"]["routes"]))
        discovery.validate_policy(index=self.index)

    def test_ireland_scope_fingerprints_match_committed_objects(self) -> None:
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
            binding_sha = hashlib.sha256(
                canonical({"basis_sha256": basis_sha, "scope": entry["scope"]})
            ).hexdigest()
            if basis_sha != entry["basis_sha256"]:
                failures.append((route, "basis", basis_sha, entry["basis_sha256"]))
            if binding_sha != entry["binding_sha256"]:
                failures.append((route, "binding", binding_sha, entry["binding_sha256"]))
        self.assertEqual([], failures)

    def test_ireland_aliases_do_not_collapse_northern_ireland(self) -> None:
        cases = {
            "support in Republic of Ireland": (["Republic of Ireland"], False),
            "support in Ireland": (["Republic of Ireland"], False),
            "support in Northern Ireland": (["Northern Ireland"], False),
            "I live in Northern Ireland but work in Ireland": ([], True),
        }
        failures = [
            (query, discovery.requested_jurisdiction(query), expected)
            for query, expected in cases.items()
            if discovery.requested_jurisdiction(query) != expected
        ]
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

    def test_cross_border_and_clinical_hostile_controls(self) -> None:
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
                failures.append((case["query"], "forbidden routes leaked", leaked))
        self.assertEqual([], failures)

    def test_ireland_python_and_browser_decision_traces_match_exactly(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required for Ireland browser decision-trace parity")

        queries = [case["query"] for case in self.benchmark["cases"]]
        queries.extend(case["query"] for case in self.benchmark["hostile_controls"])
        queries.extend([
            "support in Republic of Ireland",
            "support in Ireland",
            "support in Northern Ireland",
            "I live in Northern Ireland but work in Ireland",
        ])
        queries = list(dict.fromkeys(queries))
        payload = json.loads(discovery.browser_index_json())

        python_outputs = []
        for query in queries:
            trace, results = discovery.evaluate(query, limit=5, index=self.index)
            python_outputs.append({
                "trace": trace,
                "results": [dataclasses.asdict(result) for result in results],
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
        browser_outputs = json.loads(completed.stdout)
        self.assertEqual(python_outputs, browser_outputs)

    def test_ireland_resources_are_reviewed_claimless_first_party_navigation(self) -> None:
        failures = []
        for resource_id in IRELAND_RESOURCE_IDS:
            path = ROOT / "objects" / "resources" / f"{resource_id}.json"
            document = json.loads(path.read_text(encoding="utf-8"))
            if document["status"] != "reviewed":
                failures.append((resource_id, "status", document["status"]))
            if document["claims"] != []:
                failures.append((resource_id, "claims", document["claims"]))
            urls = [loc["value"] for loc in document["locators"] if loc["type"] == "url"]
            if not urls or not all(url.startswith("https://") for url in urls):
                failures.append((resource_id, "locators"))
            if "Republic of Ireland" not in document["audience_or_context"]:
                failures.append((resource_id, "scope wording"))
        self.assertEqual([], failures)

    def test_child_adhd_route_remains_deliberately_deferred(self) -> None:
        self.assertFalse((ROOT / "objects" / "questions" / "child-adhd-assessment-republic-ireland.json").exists())
        self.assertNotIn(
            "/questions/child-adhd-assessment-republic-ireland/",
            self.extension["scope_provenance"]["routes"],
        )
        self.assertNotIn(
            "/questions/child-adhd-assessment-republic-ireland/",
            self.extension["intent_phrases"],
        )

    def test_accepted_ireland_production_pointer_is_exact_verified_package(self) -> None:
        current = json.loads(CURRENT_PRODUCTION.read_text(encoding="utf-8"))
        self.assertEqual("94d1ab0d8df5699b1316e64d70c28fe11b25b7cf", current["source_sha"])
        self.assertEqual(325, current["corpus"]["governed_objects"])
        self.assertEqual(409, current["verification"]["canonical_routes_verified"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md",
            current["production_state_document"],
        )

    def test_ranking_and_frozen_policy_file_are_not_rewritten(self) -> None:
        frozen = json.loads(BASE_POLICY.read_text(encoding="utf-8"))
        self.assertEqual("1.1", frozen["version"])
        self.assertEqual(41, len(frozen["scope_provenance"]["routes"]))
        self.assertEqual(
            ["England", "Scotland", "Wales", "Northern Ireland"],
            frozen["jurisdiction"]["canonical_order"],
        )
        self.assertNotIn("Republic of Ireland", frozen["jurisdiction"]["scope_sets"])
        self.assertFalse(frozen["orientation"]["enabled"])


if __name__ == "__main__":
    unittest.main()
