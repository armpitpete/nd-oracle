from __future__ import annotations

import html
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_site

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "contracts" / "public-compatibility-v1.json").read_text(encoding="utf-8"))
V08_RESOURCE_IDS = set(FIXTURE["v08"]["resource_ids"])
V08_QUESTION_IDS = set(FIXTURE["v08"]["question_ids"])


class ContentNavigationV08CompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.resources = build_site.load_resources()
        self.questions = build_site.load_questions()
        self.resource_map = {resource["id"]: resource for resource in self.resources}
        self.question_map = {question["id"]: question for question in self.questions}

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_accepted_v08_object_set_remains_present(self) -> None:
        self.assertTrue(V08_RESOURCE_IDS <= set(self.resource_map))
        self.assertTrue(V08_QUESTION_IDS <= set(self.question_map))
        for resource_id in V08_RESOURCE_IDS:
            self.assertEqual("reviewed", self.resource_map[resource_id]["status"])

    def test_v08_compatibility_does_not_freeze_resources_as_permanently_claimless(self) -> None:
        claim_bearing = {rid for rid in V08_RESOURCE_IDS if self.resource_map[rid].get("claims")}
        self.assertEqual({"access-to-work", "acas-reasonable-adjustments", "disabled-students-allowance"}, claim_bearing)
        for resource_id in V08_RESOURCE_IDS - claim_bearing:
            self.assertEqual([], self.resource_map[resource_id]["claims"])

    def test_primary_navigation_preserves_v08_content_names(self) -> None:
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/questions/">Questions</a>', page)
        self.assertIn('href="/understand/">Topics</a>', page)
        self.assertIn('href="/resources/">Resources</a>', page)
        self.assertIn("Tools &amp; practical help", page)
        self.assertNotIn('>Explore</a>', page)

    def test_resource_navigation_preserves_books_media_route(self) -> None:
        resources = (self.output / "resources" / "index.html").read_text(encoding="utf-8")
        books = (self.output / "books-media" / "index.html").read_text(encoding="utf-8")
        for href in ("/resources/", "/tools/", "/games/", "/books-media/", "/community/"):
            self.assertIn(f'href="{href}"', resources)
        self.assertIn("<h1>Books &amp; media</h1>", books)

    def test_v08_cross_link_example_remains_live(self) -> None:
        concept = (self.output / "understand" / "dyslexia" / "index.html").read_text(encoding="utf-8")
        resource = (self.output / "resources" / "british-dyslexia-association" / "index.html").read_text(encoding="utf-8")
        question = (self.output / "questions" / "dyslexia-information-and-support-uk" / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/resources/british-dyslexia-association/"', concept)
        self.assertIn('href="/questions/dyslexia-information-and-support-uk/"', concept)
        self.assertIn('href="/questions/dyslexia-information-and-support-uk/"', resource)
        self.assertIn('href="/understand/dyslexia/"', question)
        self.assertIn('href="/resources/british-dyslexia-association/"', question)

    def test_all_v08_detail_routes_remain_in_current_sitemap(self) -> None:
        paths = set(build_site.sitemap_paths(build_site.load_concepts(), self.resources, self.questions))
        self.assertIn("/books-media/", paths)
        for resource_id in V08_RESOURCE_IDS:
            self.assertIn(f"/resources/{resource_id}/", paths)
        for question_id in V08_QUESTION_IDS:
            self.assertIn(f"/questions/{question_id}/", paths)
        self.assertGreaterEqual(len(paths), FIXTURE["v08"]["route_count"])

    def test_v08_question_boundary_remains_visible_for_original_questions(self) -> None:
        for question_id in V08_QUESTION_IDS:
            page = (self.output / "questions" / question_id / "index.html").read_text(encoding="utf-8")
            self.assertIn("Relevant to inspect, not recommended.", page)
            self.assertIn("Current understanding", page)
            self.assertIn("What evidence is still needed", page)
            self.assertIn(html.escape(self.question_map[question_id]["question"], quote=True), page)


if __name__ == "__main__":
    unittest.main()
