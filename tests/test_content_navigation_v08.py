from __future__ import annotations

import html
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, verify_live_site


NEW_RESOURCE_IDS = {
    "british-dyslexia-association",
    "tourettes-action",
    "mencap",
    "radld",
    "speech-and-language-uk-adult-dld-support",
    "abilitynet-my-computer-my-way",
    "acas-reasonable-adjustments",
    "disabled-students-allowance",
    "scope-support-to-work",
    "nhs-dyspraxia-adults",
}

NEW_QUESTION_IDS = {
    "dyslexia-information-and-support-uk",
    "tourette-information-and-support-uk",
    "learning-disability-information-and-support-uk",
    "dld-information-and-support",
    "make-device-easier-to-use",
    "reasonable-adjustments-at-work-great-britain",
    "disabled-student-support-england",
    "disabled-person-looking-for-work-uk",
    "adult-dyspraxia-information-uk",
}


class ContentNavigationV08Tests(unittest.TestCase):
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

    def test_v08_content_batch_is_present_and_claimless(self) -> None:
        self.assertEqual(25, len(self.resources))
        self.assertEqual(14, len(self.questions))
        self.assertTrue(NEW_RESOURCE_IDS <= set(self.resource_map))
        self.assertTrue(NEW_QUESTION_IDS <= set(self.question_map))
        for resource_id in NEW_RESOURCE_IDS:
            resource = self.resource_map[resource_id]
            self.assertEqual("reviewed", resource["status"])
            self.assertEqual([], resource["claims"])
            self.assertEqual("editor_reviewed", resource["provenance"]["review_state"])

    def test_question_navigation_groups_exactly_cover_corpus(self) -> None:
        build_site.validate_question_navigation(self.questions)
        grouped = [question_id for _group, ids in build_site.QUESTION_GROUPS for question_id in ids]
        self.assertEqual(len(self.questions), len(grouped))
        self.assertEqual({question["id"] for question in self.questions}, set(grouped))

    def test_question_index_is_grouped_and_every_question_is_reachable(self) -> None:
        page = (self.output / "questions" / "index.html").read_text(encoding="utf-8")
        for group, ids in build_site.QUESTION_GROUPS:
            self.assertIn(html.escape(group, quote=True), page)
            for question_id in ids:
                question = self.question_map[question_id]
                self.assertIn(f'href="/questions/{question_id}/"', page)
                self.assertIn(html.escape(question["question"], quote=True), page)

    def test_primary_navigation_uses_content_names_not_internal_product_terms(self) -> None:
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/questions/">Questions</a>', page)
        self.assertIn('href="/understand/">Topics</a>', page)
        self.assertIn('href="/resources/">Resources</a>', page)
        self.assertIn("Tools &amp; practical help", page)
        self.assertNotIn('>Explore</a>', page)

    def test_resource_navigation_includes_books_media(self) -> None:
        resources = (self.output / "resources" / "index.html").read_text(encoding="utf-8")
        tools = (self.output / "tools" / "index.html").read_text(encoding="utf-8")
        books = (self.output / "books-media" / "index.html").read_text(encoding="utf-8")
        self.assertIn("<h1>Resources</h1>", resources)
        self.assertIn("<h1>Tools &amp; practical help</h1>", tools)
        for href in ("/resources/", "/tools/", "/games/", "/books-media/", "/community/"):
            self.assertIn(f'href="{href}"', resources)
        self.assertIn("<h1>Books &amp; media</h1>", books)
        for resource in self.resources:
            if resource["category"] in build_site.BOOK_MEDIA_CATEGORIES:
                self.assertIn(html.escape(resource["name"], quote=True), books)

    def test_topic_resource_and_question_pages_cross_link(self) -> None:
        concept = (self.output / "understand" / "dyslexia" / "index.html").read_text(encoding="utf-8")
        resource = (
            self.output / "resources" / "british-dyslexia-association" / "index.html"
        ).read_text(encoding="utf-8")
        question = (
            self.output / "questions" / "dyslexia-information-and-support-uk" / "index.html"
        ).read_text(encoding="utf-8")

        self.assertIn("Useful next routes", concept)
        self.assertIn('href="/resources/british-dyslexia-association/"', concept)
        self.assertIn('href="/questions/dyslexia-information-and-support-uk/"', concept)

        self.assertIn("Questions that lead here", resource)
        self.assertIn('href="/questions/dyslexia-information-and-support-uk/"', resource)

        self.assertIn('href="/understand/dyslexia/"', question)
        self.assertIn('href="/resources/british-dyslexia-association/"', question)

    def test_every_resource_and_question_detail_route_is_in_sitemap(self) -> None:
        paths = set(build_site.sitemap_paths(build_site.load_concepts(), self.resources, self.questions))
        self.assertIn("/books-media/", paths)
        for resource in self.resources:
            self.assertIn(f"/resources/{resource['id']}/", paths)
        for question in self.questions:
            self.assertIn(f"/questions/{question['id']}/", paths)

    def test_live_verifier_derives_complete_v08_route_set_from_corpus(self) -> None:
        self.assertEqual(len(self.resources), len(verify_live_site.RESOURCE_MARKERS_V08))
        self.assertEqual(len(self.questions), len(verify_live_site.QUESTION_MARKERS))
        self.assertEqual(62, len(verify_live_site.V08_ROUTES))
        self.assertEqual(62, len({path for path, _marker in verify_live_site.V08_ROUTES}))
        self.assertIn("/books-media/", {path for path, _marker in verify_live_site.V08_ROUTES})
        for resource_id in NEW_RESOURCE_IDS:
            self.assertIn(f"/resources/{resource_id}/", verify_live_site.RESOURCE_MARKERS_V08)
        for question_id in NEW_QUESTION_IDS:
            self.assertIn(f"/questions/{question_id}/", verify_live_site.QUESTION_MARKERS)

    def test_v08_contracts_accept_the_actual_built_site(self) -> None:
        origin = "https://ndoracle.org"

        def fetcher(url: str):
            path = url.removeprefix(origin)
            if path == "/":
                target = self.output / "index.html"
            else:
                target = self.output / path.strip("/") / "index.html"
            self.assertTrue(target.is_file(), target)
            return verify_live_site.Response(
                status=200,
                final_url=url,
                content_type="text/html; charset=utf-8",
                body=target.read_text(encoding="utf-8"),
                headers=dict(verify_live_site.SECURITY_HEADERS),
            )

        self.assertEqual([], verify_live_site.verify_v08_question_contract(origin, fetcher=fetcher))
        self.assertEqual([], verify_live_site.verify_v08_resource_contract(origin, fetcher=fetcher))
        self.assertEqual([], verify_live_site.verify_v08_navigation_contract(origin, fetcher=fetcher))


if __name__ == "__main__":
    unittest.main()
