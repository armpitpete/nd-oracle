from __future__ import annotations

import html
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, terminology

ROOT = Path(__file__).resolve().parents[1]


class TerminologyAccessibilityV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = terminology.load_registry()
        terminology.validate_registry(cls.registry)
        cls.entries = cls.registry["entries"]
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "site"
        build_site.build(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def page(self, route: str) -> str:
        return (
            self.output / route.strip("/") / "index.html"
        ).read_text(encoding="utf-8")

    def test_registry_is_exactly_the_audited_52_with_unique_ids(self):
        self.assertEqual(52, len(self.entries))
        self.assertEqual(52, len({entry["id"] for entry in self.entries}))
        self.assertEqual(
            52,
            len({entry["term"].casefold() for entry in self.entries}),
        )

    def test_registry_contains_the_previous_17_guides(self):
        expected = {
            "neurodiversity",
            "executive-function",
            "sensory-processing",
            "dyslexia",
            "developmental-coordination-disorder",
            "learning-disability",
            "developmental-language-disorder",
            "dyscalculia",
            "masking",
            "autistic-burnout",
            "monotropism",
            "interoception",
            "alexithymia",
            "stimming",
            "communication-differences",
            "task-initiation",
            "sensory-overload",
        }
        self.assertTrue(expected <= {entry["id"] for entry in self.entries})

    def test_every_entry_has_parts_whole_meaning_route_and_provenance(self):
        for entry in self.entries:
            self.assertTrue(entry["parts"], entry["id"])
            self.assertTrue(entry["meaning"], entry["id"])
            self.assertTrue(entry["related_routes"], entry["id"])
            self.assertTrue(entry["provenance"], entry["id"])
            self.assertTrue(entry["reviewed_on"], entry["id"])

    def test_glossary_has_every_entry_and_is_stably_linkable(self):
        page = self.page("/glossary/")
        self.assertIn("Words made clearer", page)
        self.assertIn(
            'name="robots" content="noindex, follow"',
            page,
        )
        for entry in self.entries:
            self.assertEqual(
                1,
                page.count(f'id="term-{entry["id"]}"'),
                entry["id"],
            )
            self.assertIn(html.escape(entry["meaning"], quote=True), page)

    def test_glossary_is_outside_the_accepted_450_route_sitemap(self):
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        self.assertEqual(
            450,
            len(build_site.sitemap_paths(concepts, resources, questions)),
        )
        sitemap = (self.output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn("/glossary/", sitemap)

    def test_old_one_off_understand_example_is_removed(self):
        page = self.page("/understand/")
        self.assertNotIn('class="topic-word-example"', page)
        self.assertIn('href="/glossary/"', page)

    def test_representative_first_use_guides_cover_modes(self):
        cases = (
            ("/understand/monotropism/", "monotropism"),
            ("/understand/adhd/", "adhd"),
            ("/understand/executive-function/", "executive-function"),
            (
                "/questions/arfid-information-without-self-diagnosis/",
                "arfid",
            ),
            ("/questions/aac-and-nonspeaking-communication/", "aac"),
        )
        for route, term_id in cases:
            with self.subTest(route=route):
                page = self.page(route)
                self.assertEqual(
                    1,
                    page.count(f'data-term-id="{term_id}"'),
                )
                self.assertIn("What it means here:", page)
                self.assertIn(
                    f'href="/glossary/#term-{term_id}"',
                    page,
                )

    def test_same_term_is_explained_no_more_than_once_per_page(self):
        for path in self.output.rglob("index.html"):
            text = path.read_text(encoding="utf-8")
            for entry in self.entries:
                self.assertLessEqual(
                    text.count(f'data-term-id="{entry["id"]}"'),
                    1,
                    f"{path}: {entry['id']}",
                )

    def test_acronym_expansions_are_visible(self):
        page = self.page("/glossary/")
        expected = {
            "adhd": ("Attention", "Deficit", "Hyperactivity", "Disorder"),
            "arfid": (
                "Avoidant",
                "Restrictive",
                "Food intake",
                "Disorder",
            ),
            "aac": ("Augmentative", "Alternative", "Communication"),
        }
        for term_id, words in expected.items():
            block = page.split(
                f'id="term-{term_id}"',
                1,
            )[1].split("</article>", 1)[0]
            for word in words:
                self.assertIn(word, block)

    def test_a_z_and_navigation_expose_glossary(self):
        az = self.page("/a-z/")
        self.assertIn("Glossary terms", az)
        self.assertIn(
            '/glossary/#term-monotropism',
            az,
        )
        home = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn(
            '<a href="/glossary/">Glossary</a>',
            home,
        )

    def test_related_routes_exist_and_density_is_bounded(self):
        for entry in self.entries:
            for route in entry["related_routes"]:
                target = self.output / route.strip("/")
                if target.suffix:
                    self.assertTrue(target.is_file(), (entry["id"], route))
                else:
                    self.assertTrue(
                        (target / "index.html").is_file(),
                        (entry["id"], route),
                    )

        reading_roots = (
            self.output / "understand",
            self.output / "questions",
            self.output / "resources",
        )
        for reading_root in reading_roots:
            for path in reading_root.glob("*/index.html"):
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(
                    text.count('class="word-guide terminology-guide"'),
                    2,
                    path,
                )
                self.assertLessEqual(
                    text.count('data-term-id="'),
                    4,
                    path,
                )

    def test_first_use_guide_precedes_deeper_technical_detail(self):
        page = self.page("/understand/monotropism/")
        guide = page.index('data-term-id="monotropism"')
        technical = page.index('<details class="technical-summary">')
        self.assertLess(guide, technical)

    def test_policy_and_audit_are_present(self):
        policy = (
            ROOT / "docs" / "TERMINOLOGY_ACCESSIBILITY_POLICY_v1.md"
        ).read_text(encoding="utf-8")
        audit = (
            ROOT / "docs" / "TERMINOLOGY_AUDIT_v1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("first meaningful use", policy.casefold())
        self.assertIn("52", audit)
        self.assertIn("17", audit)
        self.assertIn("35", audit)


if __name__ == "__main__":
    unittest.main()
