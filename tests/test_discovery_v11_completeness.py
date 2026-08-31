from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "discovery-v1.json"
BROWSER = ROOT / "scripts" / "discovery_browser.js"


class DiscoveryV11CompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = discovery.build_index()
        cls.payload = json.loads(discovery.browser_index_json())
        cls.benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))

    def _python_output(self, query: str) -> dict:
        trace, results = discovery.evaluate(query, limit=5, index=self.index)
        return {
            "trace": trace,
            "results": [dataclasses.asdict(result) for result in results],
        }

    def _node_outputs(self, script: Path, queries: list[str]) -> list[dict]:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required for browser decision-trace parity")
        completed = subprocess.run(
            [node, str(script)],
            input=json.dumps({"queries": queries, "payload": self.payload, "limit": 5}),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        return json.loads(completed.stdout)

    def test_v10_fifty_case_benchmark_remains_pass(self) -> None:
        self.assertEqual(50, len(self.benchmark))
        failures = []
        for case in self.benchmark:
            trace, results = discovery.evaluate(case["query"], limit=5, index=self.index)
            if case["mode"] == "no_answer":
                if results:
                    failures.append((case["query"], "expected no_answer", results[0].route))
                continue
            if not results:
                failures.append((case["query"], "expected covered", trace["final_reason"]))
                continue
            if results[0].route not in case["acceptable_routes"]:
                failures.append((case["query"], results[0].route, case["acceptable_routes"]))
        self.assertEqual([], failures)

    def test_v10_benchmark_is_in_exact_python_browser_trace_parity(self) -> None:
        queries = [case["query"] for case in self.benchmark]
        python_outputs = [self._python_output(query) for query in queries]
        browser_outputs = self._node_outputs(BROWSER, queries)
        self.assertEqual(python_outputs, browser_outputs)

    def test_scope_provenance_tolerates_unrelated_object_field_change(self) -> None:
        entries = discovery.POLICY["scope_provenance"]["routes"]
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            for route in entries:
                kind, object_id = route.strip("/").split("/")
                source = ROOT / "objects" / kind / f"{object_id}.json"
                target = temp_root / "objects" / kind / f"{object_id}.json"
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            route = sorted(entries)[0]
            kind, object_id = route.strip("/").split("/")
            target = temp_root / "objects" / kind / f"{object_id}.json"
            document = json.loads(target.read_text(encoding="utf-8"))
            basis_path = entries[route]["basis_path"]
            before = discovery._resolve_json_pointer(document, basis_path)
            before_sha = hashlib.sha256(discovery._canonical_json_bytes(before)).hexdigest()
            document["_acceptance_unrelated_field"] = "must not affect routing scope provenance"
            target.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            after = discovery._resolve_json_pointer(document, basis_path)
            after_sha = hashlib.sha256(discovery._canonical_json_bytes(after)).hexdigest()
            self.assertEqual(before_sha, after_sha)

            original_root = discovery.ROOT
            try:
                discovery.ROOT = temp_root
                discovery.validate_policy(policy=discovery.POLICY, index=self.index)
            finally:
                discovery.ROOT = original_root

    def test_generated_find_js_executes_v11_policy_on_representative_cases(self) -> None:
        queries = [
            "what is autism",
            "how do I get an adult autism assessment in England",
            "Should I take more ADHD medication?",
            "disabled concessionary travel Scotland",
            "I live in Scotland but work in England",
            "how do I make tea",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            destination = build_site.build(Path(tmp) / "dist")
            generated = destination / "find.js"
            self.assertEqual(BROWSER.read_text(encoding="utf-8"), generated.read_text(encoding="utf-8"))
            python_outputs = [self._python_output(query) for query in queries]
            generated_outputs = self._node_outputs(generated, queries)
            self.assertEqual(python_outputs, generated_outputs)


if __name__ == "__main__":
    unittest.main()
