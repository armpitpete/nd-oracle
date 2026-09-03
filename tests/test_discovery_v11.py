from __future__ import annotations

import copy
import dataclasses
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "discovery-v1.1-acceptance.json"
BASE_POLICY = ROOT / "discovery" / "routing-policy-v1.1.json"
BROWSER = ROOT / "scripts" / "discovery_browser.js"
NATIONS = ("England", "Scotland", "Wales", "Northern Ireland")


class DiscoveryV11AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.index = discovery.build_index()
        cls.payload = json.loads(discovery.browser_index_json())

    def _evaluate_json(self, query: str) -> dict:
        trace, results = discovery.evaluate(query, limit=5, index=self.index)
        return {
            "trace": trace,
            "results": [dataclasses.asdict(result) for result in results],
        }

    def _conflict_queries(self) -> list[tuple[str, str, str]]:
        scope_sets = {
            name: set(values)
            for name, values in discovery.POLICY["jurisdiction"]["scope_sets"].items()
        }
        rows: list[tuple[str, str, str]] = []
        for route, (scope, stem) in self.fixture["scoped_routes"].items():
            for nation in NATIONS:
                if nation not in scope_sets[scope]:
                    rows.append((route, nation, f"{stem} {nation}"))
        return rows

    def test_policy_provenance_is_exact_and_fails_closed_on_drift(self) -> None:
        discovery.validate_policy(index=self.index)
        frozen_policy = json.loads(BASE_POLICY.read_text(encoding="utf-8"))
        entries = frozen_policy["scope_provenance"]["routes"]
        self.assertEqual(41, len(entries))
        for route, entry in entries.items():
            self.assertEqual(
                {"scope", "basis_path", "basis_sha256", "binding_sha256"},
                set(entry),
                route,
            )

        route = sorted(entries)[0]

        tampered_basis = copy.deepcopy(discovery.POLICY)
        tampered_basis["scope_provenance"]["routes"][route]["basis_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Scope declaration binding mismatch"):
            discovery.validate_policy(policy=tampered_basis, index=self.index)

        tampered_scope = copy.deepcopy(discovery.POLICY)
        current = tampered_scope["scope_provenance"]["routes"][route]["scope"]
        replacement = "England" if current != "England" else "Scotland"
        tampered_scope["scope_provenance"]["routes"][route]["scope"] = replacement
        with self.assertRaisesRegex(ValueError, "Scope declaration binding mismatch"):
            discovery.validate_policy(policy=tampered_scope, index=self.index)

        tampered_path = copy.deepcopy(discovery.POLICY)
        tampered_path["scope_provenance"]["routes"][route]["basis_path"] = "/not_a_governed_field"
        with self.assertRaisesRegex(ValueError, "Scope provenance basis missing"):
            discovery.validate_policy(policy=tampered_path, index=self.index)

    def test_frozen_clinical_acceptance_40_of_40_and_zero_of_16_false_refusals(self) -> None:
        failures = []
        for query in self.fixture["clinical"]["diagnosis"]:
            actual = discovery.clinical_boundary(query)
            if actual != "clinical_diagnosis_boundary":
                failures.append((query, actual, "clinical_diagnosis_boundary"))
        for query in self.fixture["clinical"]["medication"]:
            actual = discovery.clinical_boundary(query)
            if actual != "clinical_medication_boundary":
                failures.append((query, actual, "clinical_medication_boundary"))
        self.assertEqual([], failures)

        false_refusals = [
            (query, discovery.clinical_boundary(query))
            for query in self.fixture["clinical"]["educational_controls"]
            if discovery.clinical_boundary(query) is not None
        ]
        self.assertEqual([], false_refusals)

    def test_clinical_rule_shape_invariants(self) -> None:
        cases = {
            "Does my child have ADHD?": "clinical_diagnosis_boundary",
            "Should my child take more ADHD medication?": "clinical_medication_boundary",
            "What does ADHD mean for my child at school?": None,
            "My doctor changed my dose; where can I read general guidance?": None,
            "I am not asking whether I have ADHD; what is ADHD?": None,
            'The article says "Do I have ADHD?"; where can I read about diagnosis?': None,
            "Please, could you tell whether I am autistic?": "clinical_diagnosis_boundary",
            "What is ADHD? But should I increase my ADHD medication?": "clinical_medication_boundary",
        }
        failures = [
            (query, discovery.clinical_boundary(query), expected)
            for query, expected in cases.items()
            if discovery.clinical_boundary(query) != expected
        ]
        self.assertEqual([], failures)

    def test_jurisdiction_extraction_and_ambiguity_invariants(self) -> None:
        cases = {
            "support in England": (["England"], False),
            "support in Scotland": (["Scotland"], False),
            "support in England and Wales": (["England", "Wales"], False),
            "support in Great Britain": (["England", "Scotland", "Wales"], False),
            "support in the United Kingdom": (["England", "Scotland", "Wales", "Northern Ireland"], False),
            "GOV.UK ADHD guidance": ([], False),
            "ADHD guidance": ([], False),
            "I live in Scotland but work in England": ([], True),
            "moving from Scotland to England": ([], True),
            "England Scotland support": ([], True),
            "England Wales support": (["England", "Wales"], False),
        }
        failures = [
            (query, discovery.requested_jurisdiction(query), expected)
            for query, expected in cases.items()
            if discovery.requested_jurisdiction(query) != expected
        ]
        self.assertEqual([], failures)

    def test_frozen_70_jurisdiction_conflicts_never_surface_incompatible_scoped_results(self) -> None:
        conflicts = self._conflict_queries()
        self.assertEqual(70, len(conflicts))
        failures = []
        for source_route, nation, query in conflicts:
            trace, results = discovery.evaluate(query, limit=5, index=self.index)
            record_trace = next(record for record in trace["records"] if record["route"] == source_route)
            if not record_trace["relevance"]["eligible"]:
                failures.append((query, "source route was not relevant", source_route))
                continue
            if record_trace["scope"]["compatible"]:
                failures.append((query, "source route remained compatible", source_route))
            if source_route in trace["survivors"]:
                failures.append((query, "incompatible source route survived", source_route))
            requested = set(trace["requested_scope"])
            for result in results:
                scope = discovery._route_scope(result.route)
                if scope is not None and not requested.issubset(set(scope)):
                    failures.append((query, "incompatible result", result.route, scope, nation))
        self.assertEqual([], failures)

    def test_orientation_ablation_passes_without_orientation(self) -> None:
        self.assertFalse(discovery.POLICY["orientation"]["enabled"])
        failures = []
        for info_query, info_route, action_query, action_route in self.fixture["orientation_pairs"]:
            _info_trace, info_results = discovery.evaluate(info_query, limit=1, index=self.index)
            _action_trace, action_results = discovery.evaluate(action_query, limit=1, index=self.index)
            info_top = info_results[0].route if info_results else None
            action_top = action_results[0].route if action_results else None
            if info_top != info_route:
                failures.append(("informational", info_query, info_top, info_route))
            if action_top != action_route:
                failures.append(("action", action_query, action_top, action_route))
        self.assertEqual([], failures)

    def test_precision_20_of_20_unrelated_controls_return_no_governed_result(self) -> None:
        failures = []
        for query in self.fixture["benign_unrelated"]:
            trace, results = discovery.evaluate(query, limit=5, index=self.index)
            if results:
                failures.append((query, trace["final_reason"], [result.route for result in results]))
        self.assertEqual([], failures)

    def test_precision_invariants_preserve_governed_single_anchor_identities(self) -> None:
        for query in ("support", "support help"):
            _trace, results = discovery.evaluate(query, limit=5, index=self.index)
            self.assertEqual([], results, query)

        expected = {
            "autism": "/understand/autism/",
            "ADHD": "/understand/adhd/",
            "DLD": "/understand/developmental-language-disorder/",
        }
        failures = []
        for query, route in expected.items():
            _trace, results = discovery.evaluate(query, limit=1, index=self.index)
            actual = results[0].route if results else None
            if actual != route:
                failures.append((query, actual, route))
        self.assertEqual([], failures)

    def test_python_and_browser_decision_traces_match_exactly(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required for browser decision-trace parity")

        queries: list[str] = []
        for group in ("diagnosis", "medication", "educational_controls"):
            queries.extend(self.fixture["clinical"][group])
        queries.extend(self.fixture["benign_unrelated"])
        for info_query, _info_route, action_query, _action_route in self.fixture["orientation_pairs"]:
            queries.extend([info_query, action_query])
        queries.extend(query for _route, _nation, query in self._conflict_queries())
        queries.extend([
            "Does my child have ADHD?",
            "Should my child take more ADHD medication?",
            "What does ADHD mean for my child at school?",
            "My doctor changed my dose; where can I read general guidance?",
            "I am not asking whether I have ADHD; what is ADHD?",
            'The article says "Do I have ADHD?"; where can I read about diagnosis?',
            "I live in Scotland but work in England",
            "moving from Scotland to England",
            "England Scotland support",
            "England Wales support",
            "GOV.UK ADHD guidance",
            "support",
            "support help",
            "DLD",
        ])
        queries = list(dict.fromkeys(queries))

        python_outputs = [self._evaluate_json(query) for query in queries]
        completed = subprocess.run(
            [node, str(BROWSER)],
            input=json.dumps({"queries": queries, "payload": self.payload, "limit": 5}),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        browser_outputs = json.loads(completed.stdout)
        self.assertEqual(python_outputs, browser_outputs)

    def test_generated_find_js_is_the_v11_browser_evaluator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = build_site.build(Path(tmp) / "dist")
            generated = (destination / "find.js").read_text(encoding="utf-8")
            expected = BROWSER.read_text(encoding="utf-8")
            self.assertEqual(expected, generated)
            find_html = (destination / "find" / "index.html").read_text(encoding="utf-8")
            self.assertIn('&quot;version&quot;:&quot;1.1&quot;', find_html)


if __name__ == "__main__":
    unittest.main()
