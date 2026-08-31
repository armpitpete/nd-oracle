from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
PROBES = [
    ["assessment", "adult autism assessment Scotland"],
    ["assessment", "adult ADHD assessment Scotland"],
    ["assessment", "adult autism assessment Wales"],
    ["assessment", "adult ADHD assessment Wales"],
    ["assessment", "adult autism assessment Northern Ireland"],
    ["assessment", "adult ADHD assessment Northern Ireland"],
    ["education", "disabled student support Scotland"],
    ["education", "disabled student support Wales"],
    ["education", "disabled student support Northern Ireland"],
    ["education", "exam adjustments Scotland neurodivergent"],
    ["education", "exam adjustments Wales neurodivergent"],
    ["work", "reasonable adjustments at work Northern Ireland"],
    ["work", "Access to Work Northern Ireland"],
    ["work", "occupational health neurodivergent adjustments"],
    ["work", "self employment disability support neurodivergent"],
    ["healthcare", "healthcare communication adjustments Scotland"],
    ["healthcare", "healthcare communication adjustments Wales"],
    ["healthcare", "healthcare communication adjustments Northern Ireland"],
    ["healthcare", "dentist communication adjustments autism"],
    ["daily life", "help remembering appointments neurodivergent"],
    ["daily life", "housework is overwhelming ADHD"],
    ["daily life", "shopping is overwhelming autism"],
    ["sensory", "clothes feel painful sensory"],
    ["sensory", "smells make me overwhelmed"],
    ["relationships", "friendship misunderstandings autism"],
    ["relationships", "conflict with partner neurodivergent communication"],
    ["money/admin", "debt paperwork disability help"],
    ["parenting", "support parenting a neurodivergent child UK"],
    ["mobility", "disabled travel support England"],
    ["education", "school transition support autism England"],
]


def _load(name: str) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "objects" / name).glob("*.json"))]


class TemporaryV12CoverageAudit(unittest.TestCase):
    def test_emit_audit(self) -> None:
        counts = {name: len(_load(name)) for name in ("concepts", "resources", "questions", "evidence")}
        rows = []
        for domain, query in PROBES:
            trace, results = discovery.evaluate(query, limit=3)
            rows.append({
                "domain": domain,
                "query": query,
                "final_reason": trace["final_reason"],
                "requested_scope": trace["requested_scope"],
                "top": results[0].route if results else None,
                "top_title": results[0].title if results else None,
                "top3": [item.route for item in results],
            })
        print("V12_COVERAGE_AUDIT_JSON=" + json.dumps({"counts": counts, "total": sum(counts.values()), "rows": rows}, ensure_ascii=False, sort_keys=True))
        self.assertEqual({"concepts": 20, "resources": 61, "questions": 41, "evidence": 3}, counts)
        expected = {
            "disabled student support Scotland": "/questions/disabled-student-support-scotland/",
            "disabled student support Wales": "/questions/disabled-student-support-wales/",
            "disabled student support Northern Ireland": "/questions/disabled-student-support-northern-ireland/",
        }
        by_query = {row["query"]: row for row in rows}
        for query, route in expected.items():
            self.assertEqual(route, by_query[query]["top"])


if __name__ == "__main__":
    unittest.main()
