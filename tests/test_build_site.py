import html
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from scripts import build_site


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        for name, value in attrs:
            if name == "href" and value:
                self.hrefs.append(value)


class WebsiteBuildTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.concepts = build_site.load_concepts()
        self.concept_map = {concept["id"]: concept for concept in self.concepts}
        self.resources = build_site.load_resources()

    def tearDown(self):
        self.tempdir.cleanup()

    def html_pages(self) -> list[Path]:
        return sorted(self.output.rglob("*.html"))

    def test_build_emits_complete_public_site(self):
        expected_routes = [
            "",
            "understand",
            "resources",
            "tools",
            "games",
            "community",
            "how-it-works",
            "about",
            "accessibility",
            "feedback",
            "privacy",
            # The not-yet-interactive Oracle route remains a compatibility page.
            "oracle",
        ]
        for route in expected_routes:
            target = self.output / "index.html" if not route else self.output / route / "index.html"
            self.assertTrue(target.is_file(), route)

        for filename in ["styles.css", "_headers", "404.html", "sitemap.xml", "robots.txt"]:
            self.assertTrue((self.output / filename).is_file(), filename)

        self.assertEqual(
            (self.output / ".nd-oracle-generated").read_text(encoding="utf-8"),
            build_site.OUTPUT_MARKER,
        )
        for concept in self.concepts:
            self.assertTrue((self.output / "understand" / concept["id"] / "index.html").is_file())
        for resource in self.resources:
            self.assertTrue((self.output / "resources" / resource["id"] / "index.html").is_file())

    def test_primary_navigation_contains_only_active_destinations(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        for slug, label in build_site.PRIMARY_NAV:
            self.assertIn(f'href="/{slug}/"', page)
            self.assertIn(label, page)
        self.assertNotIn('href="/oracle/"', page)

    def test_home_has_exactly_one_ordinary_language_question_for_every_topic(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("Start with a question", page)
        concept_ids = {concept["id"] for concept in self.concepts}
        target_ids = [target_id for _, target_id in build_site.COMMON_QUESTIONS]
        self.assertEqual(set(target_ids), concept_ids)
        self.assertEqual(len(target_ids), len(concept_ids))
        for question, target_id in build_site.COMMON_QUESTIONS:
            self.assertIn(html.escape(question, quote=True), page)
            self.assertIn(f'href="/understand/{target_id}/"', page)
        self.assertNotIn("Site Shell v0.1", page)

    def test_home_exposes_populated_ecosystem(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertGreater(len(self.resources), 0)
        self.assertIn("Explore useful things", page)
        self.assertIn(f"{len(self.resources)} reviewed resources", page)
        self.assertIn('href="/tools/"', page)
        self.assertIn('href="/games/"', page)
        self.assertIn('href="/community/"', page)
        self.assertIn('href="/resources/"', page)
        self.assertIn("A listing is not an endorsement", page)

    def test_reading_layer_exactly_covers_authoritative_concept_corpus(self):
        concept_ids = {concept["id"] for concept in self.concepts}
        self.assertEqual(set(build_site.SIMPLE_EXPLANATIONS), concept_ids)
        build_site.validate_reading_layer(self.concepts)

    def test_understand_is_reading_first_and_non_clinical(self):
        page = (self.output / "understand" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Orientation, not diagnosis", page)
        self.assertIn(f"There are {len(self.concepts)} reviewed topic pages", page)
        for concept in self.concepts:
            self.assertIn(html.escape(concept["name"]), page)
            self.assertIn(html.escape(build_site.reader_intro(concept), quote=True), page)
            self.assertIn(f'/understand/{concept["id"]}/', page)

    def test_every_topic_starts_simple_then_preserves_precise_summary(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            simple = html.escape(build_site.reader_intro(concept), quote=True)
            precise = html.escape(concept["summary"], quote=True)
            self.assertIn(simple, page)
            self.assertIn("More precise description", page)
            self.assertIn(precise, page)
            self.assertLess(page.index(simple), page.index(precise))

    def test_every_topic_exposes_last_reviewed(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            reviewed = build_site.human_date(concept["provenance"]["last_reviewed"])
            self.assertIn(f"Last reviewed: <strong>{reviewed}</strong>", page)

    def test_confidence_scale_is_explained_and_linked_from_claims(self):
        how = (self.output / "how-it-works" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="confidence"', how)
        for label in ["High", "Moderate", "Low", "Contested", "Not applicable"]:
            self.assertIn(f"<dt>{label}</dt>", how)
        self.assertIn("high confidence does not mean certainty", how)
        self.assertIn("Being listed is not being endorsed", how)
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="/how-it-works/#confidence"', page)

    def test_feedback_route_is_public_safe_and_reachable(self):
        feedback = (self.output / "feedback" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Report a problem", feedback)
        self.assertIn("https://github.com/armpitpete/nd-oracle/issues/new", feedback)
        self.assertIn("Please do not include private health information", feedback)
        self.assertIn("does not yet offer a private feedback channel", feedback)
        accessibility = (self.output / "accessibility" / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/feedback/"', accessibility)
        home = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/feedback/"', home)

    def test_claims_keep_evidence_routes_but_disclose_them_progressively(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            self.assertIn("What we can say", page)
            self.assertIn('<details class="evidence-detail">', page)
            for claim in concept["claims"]:
                self.assertIn(html.escape(claim["text"], quote=True), page)
                for source_id in claim["source_ids"]:
                    self.assertIn(f'href="#source-{source_id}"', page)
                for uncertainty_id in claim["uncertainty_ids"]:
                    self.assertIn(f'href="#uncertainty-{uncertainty_id}"', page)

    def test_perspective_evidence_links_use_citations_not_generic_source_labels(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            source_map = {source["id"]: source for source in concept["sources"]}
            for perspective in concept["perspectives"]:
                for source_id in perspective["source_ids"]:
                    self.assertIn(html.escape(source_map[source_id]["citation"], quote=True), page)
        self.assertNotIn("Evidence route: source", (self.output / "understand" / "autism" / "index.html").read_text(encoding="utf-8"))

    def test_related_concepts_use_human_names(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            for relation in concept["relations"]:
                target = self.concept_map[relation["target_id"]]
                self.assertIn(f'href="/understand/{target["id"]}/"', page)
                self.assertIn(html.escape(target["name"]), page)

    def test_resource_indexes_are_active_and_category_filtered(self):
        all_page = (self.output / "resources" / "index.html").read_text(encoding="utf-8")
        tools_page = (self.output / "tools" / "index.html").read_text(encoding="utf-8")
        games_page = (self.output / "games" / "index.html").read_text(encoding="utf-8")
        community_page = (self.output / "community" / "index.html").read_text(encoding="utf-8")
        for page in [all_page, tools_page, games_page, community_page]:
            self.assertIn("Listed, not endorsed", page)
            self.assertNotIn('name="robots" content="noindex, follow"', page)
        for resource in self.resources:
            self.assertIn(html.escape(resource["name"], quote=True), all_page)
            if resource["category"] == "game":
                self.assertIn(html.escape(resource["name"], quote=True), games_page)
            if resource["category"] in build_site.TOOL_CATEGORIES:
                self.assertIn(html.escape(resource["name"], quote=True), tools_page)
            if resource["category"] in build_site.COMMUNITY_CATEGORIES:
                self.assertIn(html.escape(resource["name"], quote=True), community_page)

    def test_every_resource_page_exposes_access_limits_costs_and_conflicts(self):
        for resource in self.resources:
            page = (self.output / "resources" / resource["id"] / "index.html").read_text(encoding="utf-8")
            self.assertIn("Listed, not endorsed", page)
            self.assertIn("Limitations and possible poor fit", page)
            self.assertIn("Cost and access notes", page)
            self.assertIn("Ownership and conflicts", page)
            self.assertIn("Evidence status", page)
            self.assertIn("This listing makes no efficacy or safety claim", page)
            reviewed = build_site.human_date(resource["provenance"]["last_reviewed"])
            self.assertIn(f"Last reviewed: <strong>{reviewed}</strong>", page)
            for locator in resource["locators"]:
                if locator["type"] == "url":
                    self.assertIn(html.escape(locator["value"], quote=True), page)

    def test_every_html_page_has_basic_accessibility_and_description(self):
        for page in self.html_pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn('class="skip-link"', text)
            self.assertIn('id="main"', text)
            self.assertIn('aria-label="Primary"', text)
            self.assertIn('name="viewport"', text)
            self.assertIn('name="description"', text)

    def test_indexable_pages_have_canonical_urls(self):
        expected_paths = build_site.sitemap_paths(self.concepts, self.resources)
        for route in expected_paths:
            if route == "/":
                page = self.output / "index.html"
            else:
                page = self.output / route.lstrip("/") / "index.html"
            text = page.read_text(encoding="utf-8")
            self.assertIn(f'rel="canonical" href="{build_site.PUBLIC_ORIGIN}{route}"', text)

    def test_oracle_compatibility_route_remains_nonindexed(self):
        page = (self.output / "oracle" / "index.html").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex, follow"', page)
        self.assertIn('href="/how-it-works/"', page)

    def test_sitemap_contains_topics_resources_and_active_ecosystem_routes(self):
        sitemap = (self.output / "sitemap.xml").read_text(encoding="utf-8")
        for path in build_site.sitemap_paths(self.concepts, self.resources):
            self.assertIn(f"<loc>{build_site.PUBLIC_ORIGIN}{path}</loc>", sitemap)
        for route in ["resources", "tools", "games", "community", "feedback"]:
            self.assertIn(f"<loc>{build_site.PUBLIC_ORIGIN}/{route}/</loc>", sitemap)
        for resource in self.resources:
            self.assertIn(f"<loc>{build_site.PUBLIC_ORIGIN}/resources/{resource['id']}/</loc>", sitemap)
        self.assertNotIn(f"<loc>{build_site.PUBLIC_ORIGIN}/oracle/</loc>", sitemap)

        robots = (self.output / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn(f"Sitemap: {build_site.PUBLIC_ORIGIN}/sitemap.xml", robots)

    def test_404_is_a_helpful_non_indexed_recovery_page(self):
        page = (self.output / "404.html").read_text(encoding="utf-8")
        self.assertIn("Page not found", page)
        self.assertIn('name="robots" content="noindex, follow"', page)
        self.assertIn('href="/understand/"', page)
        self.assertIn('href="/resources/"', page)
        self.assertIn('href="/how-it-works/"', page)
        self.assertIn('href="/feedback/"', page)

    def test_internal_navigation_targets_exist(self):
        for page in self.html_pages():
            parser = LinkCollector()
            parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.hrefs:
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or href.startswith("#"):
                    continue
                if not parsed.path.startswith("/"):
                    continue
                if parsed.path == "/":
                    target = self.output / "index.html"
                elif parsed.path.endswith("/"):
                    target = self.output / parsed.path.lstrip("/") / "index.html"
                else:
                    target = self.output / parsed.path.lstrip("/")
                self.assertTrue(target.exists(), f"{page.relative_to(self.output)} -> {href}")

    def test_public_site_requires_no_javascript_or_forms(self):
        for page in self.html_pages():
            text = page.read_text(encoding="utf-8").lower()
            self.assertNotIn("<script", text)
            self.assertNotIn("<form", text)
            self.assertNotIn("style=", text)

    def test_authoritative_concepts_are_not_modified_by_build(self):
        before = {path: path.read_bytes() for path in build_site.OBJECTS_DIR.glob("*.json")}
        build_site.build(self.output)
        after = {path: path.read_bytes() for path in before}
        self.assertEqual(before, after)

    def test_build_refuses_to_replace_unmarked_directory(self):
        unknown = Path(self.tempdir.name) / "unknown"
        unknown.mkdir()
        (unknown / "keep.txt").write_text("do not delete", encoding="utf-8")
        with self.assertRaises(ValueError):
            build_site.build(unknown)
        self.assertEqual((unknown / "keep.txt").read_text(encoding="utf-8"), "do not delete")

    def test_source_links_allow_only_http_and_https(self):
        self.assertEqual(build_site.safe_http_url("https://example.org/source"), "https://example.org/source")
        self.assertEqual(build_site.safe_http_url("http://example.org/source"), "http://example.org/source")
        self.assertIsNone(build_site.safe_http_url("javascript:alert(1)"))
        self.assertIsNone(build_site.safe_http_url("data:text/html,bad"))
        self.assertIsNone(build_site.safe_http_url("not-a-url"))


if __name__ == "__main__":
    unittest.main()
