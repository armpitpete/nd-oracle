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

    def test_home_has_exact_six_primary_categories(self):
        home = self.page("/")
        contract = build_site.load_navigation_v1_contract()
        for item in contract["primary_categories"]:
            self.assertIn(f'href="{item["target_route"]}"', home)
            self.assertIn(item["label"].replace("&", "&amp;"), home)
        self.assertEqual(6, home.count("choice-card home-category-card home-category-card--primary"))

    def test_executable_categories_match_the_contract(self):
        contract = build_site.load_navigation_v1_contract()
        expected = [
            (item["id"], item["label"], item["purpose"], item["target_route"])
            for item in contract["primary_categories"]
        ]
        self.assertEqual(expected, list(build_site.NAVIGATION_V1_PRIMARY_CATEGORIES))

    def test_global_header_is_search_plus_collapsed_menu(self):
        home = self.page("/")
        start = home.index('<nav class="primary-nav" aria-label="Primary">')
        end = home.index("</nav>", start)
        nav = home[start:end]
        before_menu = nav.split('<details class="site-menu">', 1)[0]
        self.assertIn('href="/find/"', before_menu)
        self.assertNotIn('href="/a-z/"', before_menu)
        self.assertNotIn('href="/questions/"', before_menu)
        self.assertIn('<summary>Menu</summary>', nav)
        self.assertIn('href="/a-z/"', nav)
        self.assertIn('href="/about/"', nav)

    def test_secondary_exploration_is_collapsed_by_default(self):
        home = self.page("/")
        self.assertIn('<details class="home-more">', home)
        self.assertNotIn('<details class="home-more" open', home)
        for item in build_site.load_navigation_v1_contract()["secondary_exploration"]:
            self.assertIn(f'href="{item["target_route"]}"', home)

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

    def test_six_primary_routes_reach_real_content_or_next_concrete_choice(self):
        expected = {
            "/conditions/": "/understand/autism/",
            "/everyday-help/": "/needs/work/",
            "/books-media/": "/resources/a-kind-of-spark/",
            "/games-apps/": "/resources/townscaper/",
            "/organisations/": "/resources/autistica/",
            "/questions/": "/questions/phone-calls-are-difficult/",
        }
        for route, item in expected.items():
            with self.subTest(route=route):
                self.assertIn(f'href="{item}"', self.page(route))

    def test_games_apps_route_exposes_both_game_and_app_examples(self):
        page = self.page("/games-apps/")
        self.assertIn('href="/resources/townscaper/"', page)
        self.assertIn('href="/resources/focusmate/"', page)

    def test_primary_destinations_allow_wrong_choice_recovery(self):
        contract = build_site.load_navigation_v1_contract()
        for item in contract["primary_categories"]:
            page = self.page(item["target_route"])
            self.assertIn('href="/"', page)
            self.assertIn('href="/find/"', page)

    def test_compatibility_uncertainty_route_remains_bounded(self):
        page = self.page("/start/")
        for label in (
            "Something about me",
            "Something I need help with",
            "Something to read, watch or use",
            "Somewhere or someone that can help",
        ):
            self.assertIn(label, page)
        self.assertEqual(4, page.count("home-category-card--start"))

    def test_cleared_recognition_visuals_still_render_on_specific_lists(self):
        self.assertIn('src="/resource-media/a-kind-of-spark.jpg"', self.page("/books/"))
        self.assertIn('src="/resource-media/townscaper.jpg"', self.page("/games/"))
        self.assertIn('src="/resource-media/focusmate.png"', self.page("/apps-tools/"))


if __name__ == "__main__":
    unittest.main()
