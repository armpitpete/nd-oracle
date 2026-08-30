from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "discovery-v1.json"


class DiscoveryBenchmarkV10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        cls.index = discovery.build_index()

    def test_benchmark_is_frozen_at_exactly_50_unique_cases(self) -> None:
        self.assertEqual(50, len(self.cases))
        queries = [case["query"].casefold() for case in self.cases]
        self.assertEqual(len(queries), len(set(queries)))

    def test_every_case_has_explicit_useful_decision_depth(self) -> None:
        failures = []
        for case in self.cases:
            depth = case.get("max_useful_decision_depth")
            if not isinstance(depth, int) or depth < 0:
                failures.append({"query": case.get("query"), "depth": depth})
                continue
            if case["mode"] == "covered" and depth != 1:
                failures.append({"query": case["query"], "mode": case["mode"], "depth": depth})
            if case["mode"] == "no_answer" and depth != 0:
                failures.append({"query": case["query"], "mode": case["mode"], "depth": depth})
        self.assertEqual([], failures)

    def test_covered_cases_surface_an_acceptable_governed_route_in_top_three(self) -> None:
        failures = []
        for case in self.cases:
            if case["mode"] != "covered":
                continue
            mode, results = discovery.search(case["query"], limit=3, index=self.index)
            routes = [result.route for result in results]
            acceptable = set(routes) & set(case["acceptable_routes"])
            actual_depth = 1 if mode == "results" and acceptable else None
            if mode != "results" or not acceptable or actual_depth > case["max_useful_decision_depth"]:
                failures.append({
                    "query": case["query"],
                    "mode": mode,
                    "top3": routes,
                    "acceptable": case["acceptable_routes"],
                    "actual_depth": actual_depth,
                    "maximum_depth": case["max_useful_decision_depth"],
                })
        self.assertEqual([], failures)

    def test_no_answer_cases_do_not_invent_a_route(self) -> None:
        failures = []
        for case in self.cases:
            if case["mode"] != "no_answer":
                continue
            mode, results = discovery.search(case["query"], limit=3, index=self.index)
            if mode != "no_answer" or results:
                failures.append({"query": case["query"], "mode": mode, "results": [item.route for item in results]})
        self.assertEqual([], failures)

    def test_every_benchmark_route_is_currently_governed(self) -> None:
        current = {record["route"] for record in self.index}
        expected = {route for case in self.cases for route in case["acceptable_routes"]}
        self.assertEqual(set(), expected - current)


if __name__ == "__main__":
    unittest.main()
