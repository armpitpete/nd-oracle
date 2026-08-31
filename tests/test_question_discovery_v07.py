from __future__ import annotations

import html
import importlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_site

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "contracts" / "public-compatibility-v1.json").read_text(encoding="utf-8"))
V07_QUESTION_IDS = set(FIXTURE["v07"]["question_ids"])


class QuestionDiscoveryV07CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.questions = build_site.load_questions()
        self.concepts = build_site.load_concepts()
        self.resources = build_site.load_resources()
        self.concept_map = {item["id"]: item for item in self.concepts}
        self.resource_map = {item["id"]: item for item in self.resources}
        self.question_map = {item["id"]: item for item in self.questions}

    def tearDown(self):
        self.tempdir.cleanup()

    def test_first_public_question_set_remains_in_governed_corpus(self):
        self.assertTrue(V07_QUESTION_IDS <= set(self.question_map))
        for question_id in V07_QUESTION_IDS:
            self.assertEqual("partially_resolved", self.question_map[question_id]["status"])

    def test_home_keeps_practical_discovery_before_topic_orientation(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("Start with something you need to do", page)
        self.assertIn('href="/questions/"', page)
        for question_id in V07_QUESTION_IDS:
            question = self.question_map[question_id]
            self.assertIn(html.escape(question["question"], quote=True), page)
            self.assertIn(f'href="/questions/{question_id}/"', page)
        self.assertLess(page.index("Start with something you need to do"), page.index("Start with a question"))

    def test_question_index_and_pages_preserve_governed_boundary(self):
        index = (self.output / "questions" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Relevant to inspect, not recommended.", index)
        for question in self.questions:
            page = (self.output / "questions" / question["id"] / "index.html").read_text(encoding="utf-8")
            self.assertIn("Relevant to inspect, not recommended.", page)
            self.assertIn("Current understanding", page)
            self.assertIn("Related things to inspect", page)
            self.assertIn("What evidence is still needed", page)
            self.assertIn("Where people may disagree", page)
            self.assertIn("When this answer should be revisited", page)
            self.assertIn("Question provenance and review state", page)

    def test_question_related_routes_support_current_governed_object_types(self):
        for question in self.questions:
            page = (self.output / "questions" / question["id"] / "index.html").read_text(encoding="utf-8")
            for ref in question["related_objects"]:
                if ref["type"] == "concept":
                    self.assertIn(f'href="/understand/{ref["id"]}/"', page)
                    self.assertIn(html.escape(self.concept_map[ref["id"]]["name"], quote=True), page)
                elif ref["type"] == "resource":
                    self.assertIn(f'href="/resources/{ref["id"]}/"', page)
                    self.assertIn(html.escape(self.resource_map[ref["id"]]["name"], quote=True), page)
                elif ref["type"] == "question":
                    self.assertIn(f'href="/questions/{ref["id"]}/"', page)
                    self.assertIn(html.escape(self.question_map[ref["id"]]["question"], quote=True), page)
                else:
                    self.fail(f"Unexpected public question target type: {ref['type']}")

    def test_how_it_works_explains_question_led_boundary(self):
        page = (self.output / "how-it-works" / "index.html").read_text(encoding="utf-8")
        self.assertIn("<h2>Question-led discovery</h2>", page)
        self.assertIn("not a personalised recommendation", page)

    def test_current_builder_reload_is_idempotent_without_legacy_private_modules(self):
        importlib.reload(build_site)
        importlib.reload(build_site)
        self.assertEqual(1, build_site.STATIC_PAGES["how-it-works"]["body"].count("<h2>Question-led discovery</h2>"))
        self.assertEqual(1, build_site.STATIC_PAGES["about"]["body"].count("<h2>Start with the problem, not the taxonomy</h2>"))
        with tempfile.TemporaryDirectory() as tempdir:
            build_site.build(Path(tempdir) / "dist")

    def test_build_does_not_modify_authoritative_questions(self):
        before = {path: path.read_bytes() for path in build_site.QUESTIONS_DIR.glob("*.json")}
        build_site.build(self.output)
        after = {path: path.read_bytes() for path in before}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
