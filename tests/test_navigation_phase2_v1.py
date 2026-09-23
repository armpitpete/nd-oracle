import tempfile
import unittest
from pathlib import Path

from scripts import build_site


class NavigationPhase2V1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.output = Path(cls.tempdir.name) / "dist"
        build_site.build(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def page(self, route: str) -> str:
        path = self.output / "index.html" if route == "/" else self.output / route.strip("/") / "index.html"
        self.assertTrue(path.is_file(), route)
        return path.read_text(encoding="utf-8")

    def test_home_has_exact_frozen_primary_categories(self):
        home = self.page("/")
        contract = build_site.load_navigation_v1_contract()
        for item in contract["primary_categories"]:
            self.assertIn(f'href="{item["target_route"]}"', home)
            self.assertIn(item["label"].replace("&", "&amp;"), home)
        self.assertEqual(9, home.count("choice-card home-category-card"))

    def test_alias_routes_exist_without_rewriting_frozen_sitemap_authority(self):
        canonical = set(build_site.sitemap_paths(
            build_site.load_concepts(),
            build_site.load_resources(),
            build_site.load_questions(),
        ))
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(canonical))
        for route in build_site.NAVIGATION_V1_ALIAS_ROUTES:
            page = self.page(route)
            self.assertIn('name="robots" content="noindex, follow"', page)
            self.assertNotIn(route, canonical)
            self.assertIn(f'rel="canonical" href="{build_site.PUBLIC_ORIGIN}{route}"', page)

    def test_games_remains_canonical_and_indexable(self):
        page = self.page("/games/")
        self.assertNotIn('name="robots" content="noindex, follow"', page)
        self.assertIn("/games/", set(build_site.sitemap_paths(
            build_site.load_concepts(),
            build_site.load_resources(),
            build_site.load_questions(),
        )))

    def test_category_to_item_routes_are_direct(self):
        expected = {
            "/conditions/": "/understand/autism/",
            "/books/": "/resources/a-kind-of-spark/",
            "/games/": "/resources/townscaper/",
            "/apps-tools/": "/resources/focusmate/",
            "/organisations/": "/resources/autistica/",
            "/work-education/": "/questions/workplace-support-great-britain/",
            "/health-diagnosis/": "/questions/adult-adhd-assessment-england/",
            "/daily-living/": "/questions/phone-calls-are-difficult/",
        }
        for route, item in expected.items():
            with self.subTest(route=route):
                self.assertIn(f'href="{item}"', self.page(route))

    def test_category_pages_keep_orientation_utilities(self):
        for route in build_site.NAVIGATION_V1_ALIAS_ROUTES:
            page = self.page(route)
            self.assertIn('href="/"', page)
            self.assertIn('href="/find/"', page)
            self.assertIn('href="/a-z/"', page)

    def test_uncertainty_route_has_exactly_four_simple_choices(self):
        page = self.page("/start/")
        for label in (
            "Something about me",
            "Something I need help with",
            "Something to read, watch or use",
            "Somewhere or someone that can help",
        ):
            self.assertIn(label, page)
        self.assertEqual(4, page.count("home-category-card--start"))

    def test_cleared_recognition_visuals_appear_in_category_lists(self):
        self.assertIn('src="/resource-media/a-kind-of-spark.jpg"', self.page("/books/"))
        self.assertIn('src="/resource-media/townscaper.jpg"', self.page("/games/"))
        self.assertIn('src="/resource-media/focusmate.png"', self.page("/apps-tools/"))

    def test_resources_specialist_route_uses_same_concrete_labels(self):
        page = self.page("/resources/")
        for href in ("/books/", "/games/", "/conditions/", "/apps-tools/", "/organisations/"):
            self.assertIn(f'href="{href}"', page)
        for stale in ("Conditions &amp; topics", "Support &amp; organisations"):
            self.assertNotIn(stale, page)


if __name__ == "__main__":
    unittest.main()
