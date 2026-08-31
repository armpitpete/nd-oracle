from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "need-coverage-v1.2.json"


class V12NeedCoverageBenchmarkTests(unittest.TestCase):
    def test_bounded_need_coverage_benchmark(self) -> None:
        data = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        self.assertEqual("1.2-v0.1", data["version"])
        self.assertEqual(7, len(data["cases"]))
        for case in data["cases"]:
            with self.subTest(query=case["query"]):
                trace, results = discovery.evaluate(case["query"], limit=10)
                self.assertEqual(case["expected_scope"], trace["requested_scope"])
                self.assertTrue(results)
                self.assertEqual(case["expected_top"], results[0].route)


if __name__ == "__main__":
    unittest.main()
