from __future__ import annotations

import html
import tempfile
import unittest
from pathlib import Path

from scripts import build_site


V08_RESOURCE_IDS = {
    "goblin-tools", "tiimo", "time-timer", "habitica", "unpacking", "minecraft",
    "stardew-valley", "access-to-work", "national-autistic-society", "adhd-uk",
    "autistica", "autistic-self-advocacy-network", "autistica-tips-hub",
    "molehill-mountain", "unmasking-autism", "british-dyslexia-association",
    "tourettes-action", "mencap", "radld", "speech-and-language-uk-adult-dld-support",
    "abilitynet-my-computer-my-way", "acas-reasonable-adjustments",
    "disabled-students-allowance", "scope-support-to-work", "nhs-dyspraxia-adults",
}

V08_QUESTION_IDS = {
    "task-starting-and-organisation", "low-time-pressure-games",
    "workplace-support-great-britain", "autism-information-and-support",
    "autism-anxiety-tools", "dyslexia-information-and-support-uk",
    "tourette-information-and-support-uk", "learning-disability-information-and-support-uk",
    "dld-information-and-support", "make-device-easier-to-use",
    "reasonable-adjustments-at-work-great-britain", "disabled-student-support-england",
    "disabled-person-looking-for-work-uk", "adult-dyspraxia-information-uk",
}


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
            resource = self.resource_map[resource_id]
            self.assertEqual("reviewed", resource["status"])
            self.assertEqual([], resource["claims"])

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
        resource = (
            self.output / "resources" / "british-dyslexia-association" / "index.html"
        ).read_text(encoding="utf-8")
        question = (
            self.output / "questions" / "dyslexia-information-and-support-uk" / "index.html"
        ).read_text(encoding="utf-8")
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
        self.assertGreaterEqual(len(paths), 62)

    def test_v08_question_boundary_remains_visible_for_original_questions(self) -> None:
        for question_id in V08_QUESTION_IDS:
            page = (self.output / "questions" / question_id / "index.html").read_text(encoding="utf-8")
            self.assertIn("Relevant to inspect, not recommended.", page)
            self.assertIn("Current understanding", page)
            self.assertIn("What evidence is still needed", page)
            self.assertIn(html.escape(self.question_map[question_id]["question"], quote=True), page)


if __name__ == "__main__":
    unittest.main()
