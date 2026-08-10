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

    def tearDown(self):
        self.tempdir.cleanup()

    def html_pages(self) -> list[Path]:
        return sorted(self.output.rglob("*.html"))

    def test_build_emits_complete_site_shell(self):
        expected_routes = [
            "",
            "understand",
            "tools",
            "games",
            "resources",
            "community",
            "oracle",
            "about",
            "accessibility",
            "privacy",
        ]
        for route in expected_routes:
            target = self.output / "index.html" if not route else self.output / route / "index.html"
            self.assertTrue(target.is_file(), route)

        self.assertTrue((self.output / "styles.css").is_file())
        self.assertTrue((self.output / "_headers").is_file())
        self.assertEqual(
            (self.output / ".nd-oracle-generated").read_text(encoding="utf-8"),
            build_site.OUTPUT_MARKER,
        )
        for concept in self.concepts:
            self.assertTrue((self.output / "understand" / concept["id"] / "index.html").is_file())

    def test_home_exposes_durable_top_level_structure(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("The Neurodiverse Oracle", page)
        for slug, label in build_site.PRIMARY_NAV:
            self.assertIn(f'href="/{slug}/"', page)
            self.assertIn(label, page)

    def test_understand_is_reading_first_and_non_clinical(self):
        page = (self.output / "understand" / "index.html").read_text(encoding="utf-8")
        self.assertIn("not diagnosis or medical advice", page)
        for concept in self.concepts:
            self.assertIn(html.escape(concept["name"]), page)
            self.assertIn(f'/understand/{concept["id"]}/', page)

    def test_every_claim_keeps_visible_evidence_and_uncertainty_routes(self):
        for concept in self.concepts:
            page = (self.output / "understand" / concept["id"] / "index.html").read_text(encoding="utf-8")
            for claim in concept["claims"]:
                self.assertIn(html.escape(claim["text"], quote=True), page)
                for source_id in claim["source_ids"]:
                    self.assertIn(f'href="#source-{source_id}"', page)
                for uncertainty_id in claim["uncertainty_ids"]:
                    self.assertIn(f'href="#uncertainty-{uncertainty_id}"', page)

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

    def test_site_shell_requires_no_javascript_or_forms(self):
        for page in self.html_pages():
            text = page.read_text(encoding="utf-8").lower()
            self.assertNotIn("<script", text)
            self.assertNotIn("<form", text)
            self.assertNotIn("style=", text)

    def test_accessibility_basics_are_present_on_every_page(self):
        for page in self.html_pages():
            text = page.read_text(encoding="utf-8")
            self.assertIn('class="skip-link"', text)
            self.assertIn('id="main"', text)
            self.assertIn('aria-label="Primary"', text)
            self.assertIn('name="viewport"', text)

    def test_authoritative_objects_are_not_modified_by_build(self):
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
