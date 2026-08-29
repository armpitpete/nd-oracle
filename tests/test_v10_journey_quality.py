from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery


class V10JourneyQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.dist = build_site.build(Path(cls.temp.name) / "dist")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def page(self, route: str) -> str:
        if route == "/":
            path = self.dist / "index.html"
        else:
            path = self.dist / route.strip("/") / "index.html"
        self.assertTrue(path.is_file(), route)
        return path.read_text(encoding="utf-8")

    def test_home_can_enter_local_discovery_without_taxonomy(self) -> None:
        home = self.page("/")
        self.assertIn('href="/find/"', home)
        find = self.page("/find/")
        self.assertIn("Describe the problem in your own words", find)
        self.assertIn('src="/find.js"', find)
        self.assertNotIn("<form", find.casefold())

    def test_discovery_result_routes_are_real_governed_pages(self) -> None:
        for query in ("work is too noisy", "phone calls are hard", "numbers make no sense", "help at university"):
            mode, results = discovery.search(query, limit=3)
            self.assertEqual("results", mode, query)
            self.assertTrue(results, query)
            for result in results:
                self.page(result.route)

    def test_question_routes_into_governed_objects_and_adjacent_questions(self) -> None:
        page = self.page("/questions/reasonable-adjustments-at-work-great-britain/")
        self.assertIn('href="/resources/acas-reasonable-adjustments/"', page)
        self.assertIn('href="/resources/access-to-work/"', page)
        self.assertIn('<h2 id="related-questions-heading">Related questions</h2>', page)

    def test_claim_bearing_resource_exposes_claim_evidence_uncertainty_and_confidence(self) -> None:
        page = self.page("/resources/acas-reasonable-adjustments/")
        self.assertIn("Governed claims and evidence", page)
        self.assertIn("Evidence route", page)
        self.assertIn("Uncertainty and limits", page)
        self.assertIn('href="/how-it-works/#confidence"', page)
        self.assertIn("A supported claim is not a recommendation or an individual decision.", page)
        self.assertIn("https://www.acas.org.uk/reasonable-adjustments", page)

    def test_no_answer_and_privacy_boundaries_are_visible(self) -> None:
        js = (self.dist / "find.js").read_text(encoding="utf-8")
        self.assertIn("No governed answer", js)
        self.assertIn("No governed answer yet", js)
        self.assertIn("cannot diagnose you", js)
        privacy = self.page("/privacy/")
        self.assertIn("Query text is not submitted in a URL", privacy)
        self.assertIn("sent to an AI or search service", privacy)
        headers = (self.dist / "_headers").read_text(encoding="utf-8")
        self.assertIn("script-src 'self'", headers)
        self.assertIn("connect-src 'none'", headers)
        self.assertIn("form-action 'none'", headers)

    def test_geographic_browse_keeps_devolved_systems_distinct(self) -> None:
        page = self.page("/places/")
        for heading in ("England and Wales", "Scotland", "Wales", "Northern Ireland"):
            self.assertIn(heading, page)
        self.assertIn('href="/resources/scotland-adult-disability-payment/"', page)
        self.assertIn('href="/resources/nidirect-pip/"', page)
        self.assertIn('href="/resources/wales-disabled-concessionary-travel/"', page)

    def test_only_find_page_has_a_script_element(self) -> None:
        html_files = list(self.dist.rglob("*.html"))
        scripted = []
        for path in html_files:
            if "<script" in path.read_text(encoding="utf-8").casefold():
                scripted.append(path.relative_to(self.dist).as_posix())
        self.assertEqual(["find/index.html"], sorted(scripted))


if __name__ == "__main__":
    unittest.main()
