from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import verify_live_site

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "contracts" / "public-compatibility-v1.json").read_text(encoding="utf-8"))


class VerifyQuestionDiscoveryV07CompatibilityTests(unittest.TestCase):
    def test_v07_question_ids_are_frozen_as_data_not_executable_route_tables(self):
        frozen = set(FIXTURE["v07"]["question_ids"])
        current = set(verify_live_site.QUESTION_RECORD_MAP)
        self.assertEqual(5, len(frozen))
        self.assertTrue(frozen <= current)

    def test_current_verifier_checks_frozen_compatibility_fixture(self):
        self.assertEqual([], verify_live_site.verify_compatibility_fixture())

    def test_v07_question_routes_are_still_in_current_canonical_route_set(self):
        paths = {path for path, _marker in verify_live_site.V10_ROUTES}
        self.assertIn("/questions/", paths)
        for question_id in FIXTURE["v07"]["question_ids"]:
            self.assertIn(f"/questions/{question_id}/", paths)

    def test_current_question_contract_keeps_v07_non_recommendation_boundary(self):
        origin = "https://ndoracle.org"
        frozen_paths = {f"/questions/{qid}/" for qid in FIXTURE["v07"]["question_ids"]}

        def fetcher(url: str):
            path = url.removeprefix(origin)
            if path == "/questions/":
                body = "Relevant to inspect, not recommended." + f"{len(verify_live_site.QUESTION_RECORDS)} governed practical questions" + '<a href="/needs/">Needs</a><a href="/a-z/">A-Z</a>'
            elif path in verify_live_site.QUESTION_MARKERS_V10:
                body = (
                    "Relevant to inspect, not recommended."
                    '<h2 id="current-understanding-heading">Current understanding</h2>'
                    '<h2 id="related-things-heading">Related things to inspect</h2>'
                    '<h2 id="related-questions-heading">Related questions</h2>'
                    '<h2 id="evidence-needed-heading">What evidence is still needed</h2>'
                    '<h2 id="dissent-heading">Where people may disagree</h2>'
                    '<h2 id="reopen-heading">When this answer should be revisited</h2>'
                )
            else:
                raise AssertionError(url)
            return verify_live_site.Response(200, url, "text/html; charset=utf-8", body, dict(verify_live_site.SECURITY_HEADERS))

        failures = verify_live_site.verify_v10_question_contract(origin, fetcher=fetcher)
        self.assertEqual([], failures)
        self.assertTrue(frozen_paths <= set(verify_live_site.QUESTION_MARKERS_V10))


if __name__ == "__main__":
    unittest.main()
