from __future__ import annotations

import html
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "verify_live_site.py"
SPEC = importlib.util.spec_from_file_location("verify_live_site_v07_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
verify_live_site = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verify_live_site
SPEC.loader.exec_module(verify_live_site)


class VerifyQuestionDiscoveryV07Tests(unittest.TestCase):
    def response(
        self,
        *,
        status=200,
        final_url="https://ndoracle.org/",
        content_type="text/html; charset=utf-8",
        body="",
        headers=None,
    ):
        return verify_live_site.Response(
            status=status,
            final_url=final_url,
            content_type=content_type,
            body=body,
            headers=dict(verify_live_site.SECURITY_HEADERS if headers is None else headers),
        )

    def test_v07_route_set_extends_v06_to_42_canonical_routes(self):
        old_paths = tuple(path for path, _ in verify_live_site.ROUTES)
        new_paths = tuple(path for path, _ in verify_live_site.V07_ROUTES)
        self.assertEqual(36, len(old_paths))
        self.assertEqual(42, len(new_paths))
        self.assertEqual(42, len(set(new_paths)))
        self.assertTrue(set(old_paths).issubset(new_paths))
        self.assertIn("/questions/", new_paths)
        for path in verify_live_site.QUESTION_MARKERS:
            self.assertIn(path, new_paths)

    def test_v07_question_contract_accepts_governed_static_surface(self):
        origin = "https://ndoracle.org"

        def fetcher(url):
            path = url.removeprefix(origin)
            if path == "/":
                body = "".join(
                    f'<a href="{question_path}">{html.escape(question, quote=True)}</a>'
                    for question_path, question in verify_live_site.QUESTION_MARKERS.items()
                )
            elif path == "/questions/":
                body = (
                    "Relevant to inspect, not recommended."
                    "5 governed practical questions"
                    + "".join(
                        f'<a href="{question_path}">{html.escape(question, quote=True)}</a>'
                        for question_path, question in verify_live_site.QUESTION_MARKERS.items()
                    )
                )
            elif path in verify_live_site.QUESTION_MARKERS:
                body = (
                    "Relevant to inspect, not recommended."
                    '<h2 id="current-understanding-heading">Current understanding</h2>'
                    '<h2 id="related-things-heading">Related things to inspect</h2>'
                    '<h2 id="evidence-needed-heading">What evidence is still needed</h2>'
                    '<h2 id="dissent-heading">Where people may disagree</h2>'
                    '<h2 id="reopen-heading">When this answer should be revisited</h2>'
                    '<p class="review-meta">Last reviewed: now</p>'
                    "<summary>Question provenance and review state</summary>"
                )
            elif path == "/how-it-works/":
                body = "<h2>Question-led discovery</h2>"
            else:
                raise AssertionError(url)
            return self.response(final_url=url, body=body)

        self.assertEqual(
            verify_live_site.verify_v07_question_contract(origin, fetcher=fetcher),
            [],
        )

    def test_v07_question_contract_rejects_missing_recommendation_boundary(self):
        origin = "https://ndoracle.org"

        def fetcher(url):
            path = url.removeprefix(origin)
            if path == "/":
                body = "".join(
                    f'<a href="{question_path}">{html.escape(question, quote=True)}</a>'
                    for question_path, question in verify_live_site.QUESTION_MARKERS.items()
                )
            elif path == "/questions/":
                body = (
                    "Relevant to inspect, not recommended."
                    "5 governed practical questions"
                    + "".join(
                        f'<a href="{question_path}">{html.escape(question, quote=True)}</a>'
                        for question_path, question in verify_live_site.QUESTION_MARKERS.items()
                    )
                )
            elif path in verify_live_site.QUESTION_MARKERS:
                boundary = (
                    ""
                    if path == "/questions/task-starting-and-organisation/"
                    else "Relevant to inspect, not recommended."
                )
                body = (
                    boundary
                    + '<h2 id="current-understanding-heading">Current understanding</h2>'
                    + '<h2 id="related-things-heading">Related things to inspect</h2>'
                    + '<h2 id="evidence-needed-heading">What evidence is still needed</h2>'
                    + '<h2 id="dissent-heading">Where people may disagree</h2>'
                    + '<h2 id="reopen-heading">When this answer should be revisited</h2>'
                    + '<p class="review-meta">Last reviewed: now</p>'
                    + "<summary>Question provenance and review state</summary>"
                )
            elif path == "/how-it-works/":
                body = "<h2>Question-led discovery</h2>"
            else:
                raise AssertionError(url)
            return self.response(final_url=url, body=body)

        failures = verify_live_site.verify_v07_question_contract(origin, fetcher=fetcher)
        self.assertTrue(
            any(
                "/questions/task-starting-and-organisation/" in failure
                and "Relevant to inspect" in failure
                for failure in failures
            )
        )

    def test_expected_sitemap_urls_now_include_question_routes(self):
        origin = "https://ndoracle.org"
        expected = verify_live_site.expected_sitemap_urls(origin)
        self.assertEqual(42, len(expected))
        self.assertIn(origin + "/questions/", expected)
        for path in verify_live_site.QUESTION_MARKERS:
            self.assertIn(origin + path, expected)


if __name__ == "__main__":
    unittest.main()
