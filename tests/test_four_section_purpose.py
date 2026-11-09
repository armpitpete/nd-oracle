"""Purpose and independence of the four main ND Oracle sections."""
from __future__ import annotations

import re
import unittest

from scripts import build_site

def main_html(page: str) -> str:
    match = re.search(r"<main[^>]*>(.*?)</main>", page, re.S)
    if not match:
        raise AssertionError("Missing main content")
    return match.group(1)

def links(page: str) -> list[str]:
    return re.findall(r'<a\b[^>]*href="([^"]+)"', main_html(page))

class SectionPurposeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = build_site.load_questions()
        cls.concepts = build_site.load_concepts()
        cls.resources = build_site.load_resources()

    def test_find_has_one_search_action_and_no_cross_section_prompts(self):
        page = build_site.render_find_page()
        self.assertIn("<h1>Find</h1>", page)
        self.assertIn('id="find-input"', page)
        self.assertIn('id="find-button"', page)
        self.assertEqual([], links(page))
        self.assertNotIn("Browse by", main_html(page).split("<template", 1)[0])
        self.assertIn("Search results will appear here", page)

    def test_questions_begins_with_questions_and_lists_each_once(self):
        page = build_site.render_questions_index_v2(self.questions)
        self.assertIn("<h1>Questions</h1>", page)
        self.assertIn("What do you need help with?", page)
        self.assertNotIn("question-start-card", page)
        self.assertNotIn("question-complete", page)
        self.assertEqual(len(self.questions), page.count('<article class="topic-row">'))
        self.assertTrue(all(href.startswith("/questions/") or href.startswith("#") for href in links(page)))
        for question in self.questions:
            self.assertEqual(1, links(page).count(f"/questions/{question['id']}/"))

    def test_topics_shows_each_topic_once_without_competing_catalogues(self):
        page = build_site.render_understand_index_v24(self.concepts)
        self.assertIn("<h1>Topics</h1>", page)
        self.assertIn("Choose a topic", page)
        self.assertNotIn("topic-recognition", page)
        self.assertNotIn("topic-complete", page)
        self.assertTrue(all(href.startswith("/understand/") for href in links(page)))
        for concept in self.concepts:
            self.assertEqual(1, links(page).count(f"/understand/{concept['id']}/"))

    def test_resources_excludes_conditions_and_other_section_shortcuts(self):
        page = build_site.render_resources_navigation_v1(self.resources)
        self.assertIn("<h1>Resources</h1>", page)
        self.assertNotIn('href="/conditions/"', main_html(page))
        self.assertNotIn('href="/a-z/"', main_html(page))
        self.assertEqual(1, links(page).count("/about/#resource-listings"))
        self.assertEqual(4, page.count("choice-card choice-card--family"))
        allowed={"/books-media/","/games/","/tools/","/community/","/about/#resource-listings"}
        self.assertTrue(all(href in allowed or href.startswith("/resources/") for href in links(page)))
        for resource in self.resources:
            self.assertEqual(1, links(page).count(f"/resources/{resource['id']}/"))
        self.assertIn("ND Oracle describes resources; it does not recommend them.", page)

if __name__ == "__main__":
    unittest.main()
