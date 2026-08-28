from __future__ import annotations

import html
import tempfile
import unittest
from pathlib import Path

from scripts import build_site


class QuestionDiscoveryV07Tests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.questions = build_site.load_questions()
        self.concepts = build_site.load_concepts()
        self.resources = build_site.load_resources()
        self.concept_map = {item["id"]: item for item in self.concepts}
        self.resource_map = {item["id"]: item for item in self.resources}

    def tearDown(self):
        self.tempdir.cleanup()

    def test_first_public_question_set_is_governed_and_complete(self):
        self.assertEqual(5, len(self.questions))
        self.assertEqual(
            {
                "task-starting-and-organisation",
                "low-time-pressure-games",
                "workplace-support-great-britain",
                "autism-information-and-support",
                "autism-anxiety-tools",
            },
            {question["id"] for question in self.questions},
        )

    def test_home_routes_practical_questions_before_topic_orientation(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("Start with something you need to do", page)
        self.assertIn('href="/questions/"', page)
        for question in self.questions:
            escaped = html.escape(question["question"], quote=True)
            route = f'/questions/{question["id"]}/'
            self.assertIn(escaped, page)
            self.assertIn(f'href="{route}"', page)
        self.assertLess(
            page.index("Start with something you need to do"),
            page.index("Start with a question"),
        )

    def test_question_index_is_canonical_and_preserves_boundary(self):
        page = (self.output / "questions" / "index.html").read_text(encoding="utf-8")
        self.assertIn('<link rel="canonical" href="https://ndoracle.org/questions/">', page)
        self.assertNotIn('name="robots" content="noindex, follow"', page)
        self.assertIn("Relevant to inspect, not recommended.", page)
        self.assertIn(f"{len(self.questions)} governed practical questions", page)
        for question in self.questions:
            self.assertIn(html.escape(question["question"], quote=True), page)
            self.assertIn(f'href="/questions/{question["id"]}/"', page)

    def test_each_question_page_exposes_synthesis_uncertainty_and_provenance(self):
        for question in self.questions:
            page = (
                self.output / "questions" / question["id"] / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn(
                f'<link rel="canonical" href="https://ndoracle.org/questions/{question["id"]}/">',
                page,
            )
            self.assertNotIn('name="robots" content="noindex, follow"', page)
            self.assertIn("Relevant to inspect, not recommended.", page)
            self.assertIn("Current understanding", page)
            self.assertIn(
                html.escape(question["current_understanding"], quote=True), page
            )
            self.assertIn("Related things to inspect", page)
            self.assertIn("What evidence is still needed", page)
            self.assertIn("Where people may disagree", page)
            self.assertIn("When this answer should be revisited", page)
            self.assertIn("Question provenance and review state", page)
            reviewed = build_site.human_date(question["provenance"]["last_reviewed"])
            self.assertIn(f"Last reviewed: <strong>{reviewed}</strong>", page)

    def test_question_related_routes_use_governed_object_names(self):
        for question in self.questions:
            page = (
                self.output / "questions" / question["id"] / "index.html"
            ).read_text(encoding="utf-8")
            for ref in question["related_objects"]:
                if ref["type"] == "concept":
                    target = self.concept_map[ref["id"]]
                    self.assertIn(f'href="/understand/{ref["id"]}/"', page)
                    self.assertIn(html.escape(target["name"], quote=True), page)
                elif ref["type"] == "resource":
                    target = self.resource_map[ref["id"]]
                    self.assertIn(f'href="/resources/{ref["id"]}/"', page)
                    self.assertIn(html.escape(target["name"], quote=True), page)
                else:
                    self.fail(f"Unexpected public question target type: {ref['type']}")

    def test_sitemap_includes_question_index_and_every_question(self):
        sitemap = (self.output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("<loc>https://ndoracle.org/questions/</loc>", sitemap)
        for question in self.questions:
            self.assertIn(
                f"<loc>https://ndoracle.org/questions/{question['id']}/</loc>",
                sitemap,
            )
        self.assertEqual(
            42,
            len(build_site.sitemap_paths(self.concepts, self.resources, self.questions)),
        )

    def test_how_it_works_explains_question_led_boundary(self):
        page = (self.output / "how-it-works" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("<h2>Question-led discovery</h2>", page)
        self.assertIn("not a personalised recommendation", page)

    def test_build_does_not_modify_authoritative_questions(self):
        before = {
            path: path.read_bytes()
            for path in build_site.QUESTIONS_DIR.glob("*.json")
        }
        build_site.build(self.output)
        after = {path: path.read_bytes() for path in before}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
