from __future__ import annotations

import html
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from scripts import build_site


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for name, value in attrs if name == "href" and value)


class WebsiteBuildTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.concepts = build_site.load_concepts()
        self.resources = build_site.load_resources()
        self.questions = build_site.load_questions()
        self.evidence = build_site.load_evidence()
        self.concept_map = {item["id"]: item for item in self.concepts}

    def tearDown(self):
        self.tempdir.cleanup()

    def html_pages(self) -> list[Path]:
        return sorted(self.output.rglob("*.html"))

    def page(self, route: str) -> str:
        target = self.output / "index.html" if route == "/" else self.output / route.strip("/") / "index.html"
        self.assertTrue(target.is_file(), target)
        return target.read_text(encoding="utf-8")

    def test_build_emits_complete_current_surface(self):
        for route in ("/", "/understand/", "/resources/", "/tools/", "/games/", "/community/", "/books-media/", "/questions/", "/needs/", "/types/", "/places/", "/a-z/", "/find/", "/how-it-works/", "/about/", "/accessibility/", "/feedback/", "/privacy/", "/oracle/"):
            self.page(route)
        for filename in ("styles.css", "_headers", "find.js", "404.html", "sitemap.xml", "robots.txt"):
            self.assertTrue((self.output / filename).is_file(), filename)
        self.assertEqual(build_site.OUTPUT_MARKER, (self.output / ".nd-oracle-generated").read_text(encoding="utf-8"))
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(build_site.sitemap_paths(self.concepts, self.resources, self.questions)))

    def test_primary_navigation_contains_only_active_destinations(self):
        page = self.page("/")
        for slug, label in build_site.PRIMARY_NAV:
            self.assertIn(f'href="/{slug}/"', page); self.assertIn(label, page)
        self.assertNotIn('href="/oracle/"', page)
        self.assertIn('href="/find/"', page)

    def test_home_has_one_ordinary_language_route_for_every_topic(self):
        page = self.page("/"); concept_ids = {item["id"] for item in self.concepts}; target_ids = [target for _q, target in build_site.COMMON_QUESTIONS]
        self.assertEqual(concept_ids, set(target_ids)); self.assertEqual(len(concept_ids), len(target_ids))
        for question, target in build_site.COMMON_QUESTIONS:
            self.assertIn(html.escape(question, quote=True), page); self.assertIn(f'href="/understand/{target}/"', page)

    def test_reading_layer_and_topic_evidence_routes_cover_current_concepts(self):
        self.assertEqual({item["id"] for item in self.concepts}, set(build_site.SIMPLE_EXPLANATIONS)); build_site.validate_reading_layer(self.concepts)
        for concept in self.concepts:
            page = self.page(f'/understand/{concept["id"]}/')
            simple = html.escape(build_site.reader_intro(concept), quote=True); precise = html.escape(concept["summary"], quote=True)
            self.assertIn(simple, page); self.assertIn(precise, page); self.assertLess(page.index(simple), page.index(precise))
            self.assertIn('href="/how-it-works/#confidence"', page)
            self.assertIn("Last reviewed: <strong>", page)
            for claim in concept["claims"]:
                self.assertIn(html.escape(claim["text"], quote=True), page)
                for source_id in claim["source_ids"]: self.assertIn(f'href="#source-{source_id}"', page)
                for uncertainty_id in claim["uncertainty_ids"]: self.assertIn(f'href="#uncertainty-{uncertainty_id}"', page)
            source_map = {source["id"]: source for source in concept["sources"]}
            for perspective in concept["perspectives"]:
                for source_id in perspective["source_ids"]:
                    self.assertIn(html.escape(source_map[source_id]["citation"], quote=True), page)
            for relation in concept["relations"]:
                target = self.concept_map[relation["target_id"]]
                self.assertIn(f'href="/understand/{target["id"]}/"', page)
                self.assertIn(html.escape(target["name"], quote=True), page)

    def test_confidence_scale_and_non_endorsement_boundary_are_explained(self):
        how = self.page("/how-it-works/")
        self.assertIn('id="confidence"', how)
        for label in ("High", "Moderate", "Low", "Contested", "Not applicable"):
            self.assertIn(f"<dt>{label}</dt>", how)
        self.assertIn("high confidence does not mean certainty", how)
        self.assertIn("Being listed is not being endorsed", how)
        self.assertIn("Governed discovery", how)

    def test_resource_indexes_are_active_and_category_filtered(self):
        all_page, tools, games, community = self.page("/resources/"), self.page("/tools/"), self.page("/games/"), self.page("/community/")
        for page in (all_page, tools, games, community): self.assertIn("Listed, not endorsed", page)
        for resource in self.resources:
            name = html.escape(resource["name"], quote=True); self.assertIn(name, all_page)
            if resource["category"] == "game": self.assertIn(name, games)
            if resource["category"] in build_site.TOOL_CATEGORIES: self.assertIn(name, tools)
            if resource["category"] in build_site.COMMUNITY_CATEGORIES: self.assertIn(name, community)

    def test_every_resource_page_exposes_access_limits_scope_costs_conflicts_and_correct_claim_boundary(self):
        for resource in self.resources:
            page = self.page(f'/resources/{resource["id"]}/')
            for marker in ("Listed, not endorsed", "Limitations and possible poor fit", "Cost and access notes", "Ownership and conflicts", "Evidence status", "Scope for navigation", "Questions that lead here"):
                self.assertIn(marker, page)
            if resource.get("claims"):
                self.assertIn("Governed claims and evidence", page); self.assertIn("Evidence route", page); self.assertIn("Uncertainty and limits", page)
                self.assertIn("A supported claim is not a recommendation or an individual decision.", page)
            else:
                self.assertIn("This listing makes no efficacy or safety claim", page)
            for locator in resource["locators"]:
                if locator["type"] == "url": self.assertIn(html.escape(locator["value"], quote=True), page)

    def test_claim_bearing_resources_reference_governed_evidence(self):
        evidence_ids = {item["id"] for item in self.evidence}; claim_count = 0
        for resource in self.resources:
            for claim in resource.get("claims", []):
                claim_count += 1; self.assertTrue(set(claim["evidence_ids"]) <= evidence_ids)
        self.assertGreaterEqual(claim_count, 3)

    def test_questions_expose_bounded_synthesis_and_related_navigation(self):
        build_site.validate_question_navigation(self.questions)
        index = self.page("/questions/"); self.assertIn("Relevant to inspect, not recommended.", index)
        for question in self.questions:
            page = self.page(f'/questions/{question["id"]}/')
            for marker in ("Relevant to inspect, not recommended.", "Current understanding", "Related things to inspect", "Related questions", "What evidence is still needed", "Where people may disagree", "When this answer should be revisited", "Question provenance and review state"):
                self.assertIn(marker, page)

    def test_every_indexable_page_has_accessibility_metadata_and_canonical_url(self):
        paths = build_site.sitemap_paths(self.concepts, self.resources, self.questions)
        for route in paths:
            text = self.page(route)
            for marker in ('class="skip-link"', 'id="main"', 'aria-label="Primary"', 'name="viewport"', 'name="description"'):
                self.assertIn(marker, text)
            self.assertIn(f'rel="canonical" href="{build_site.PUBLIC_ORIGIN}{route}"', text)
            self.assertNotIn('name="robots" content="noindex, follow"', text)

    def test_oracle_and_404_are_nonindexed_recovery_surfaces(self):
        oracle = self.page("/oracle/"); self.assertIn('name="robots" content="noindex, follow"', oracle); self.assertIn('href="/how-it-works/"', oracle)
        missing = (self.output / "404.html").read_text(encoding="utf-8"); self.assertIn("Page not found", missing); self.assertIn('name="robots" content="noindex, follow"', missing)

    def test_sitemap_and_robots_match_current_canonical_set(self):
        paths = build_site.sitemap_paths(self.concepts, self.resources, self.questions); sitemap = (self.output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(paths)); self.assertEqual(len(paths), len(set(paths)))
        for path in paths: self.assertIn(f"<loc>{build_site.PUBLIC_ORIGIN}{path}</loc>", sitemap)
        self.assertNotIn(f"<loc>{build_site.PUBLIC_ORIGIN}/oracle/</loc>", sitemap)
        robots = (self.output / "robots.txt").read_text(encoding="utf-8"); self.assertIn("User-agent: *", robots); self.assertIn(f"Sitemap: {build_site.PUBLIC_ORIGIN}/sitemap.xml", robots)

    def test_internal_navigation_targets_exist(self):
        for page in self.html_pages():
            parser = LinkCollector(); parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.hrefs:
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or href.startswith("#") or not parsed.path.startswith("/"): continue
                target = self.output / "index.html" if parsed.path == "/" else (self.output / parsed.path.lstrip("/") / "index.html" if parsed.path.endswith("/") else self.output / parsed.path.lstrip("/"))
                self.assertTrue(target.exists(), f"{page.relative_to(self.output)} -> {href}")

    def test_public_site_allows_only_the_local_find_script_and_no_forms(self):
        scripted = []
        for page in self.html_pages():
            text = page.read_text(encoding="utf-8").lower(); self.assertNotIn("<form", text); self.assertNotIn("style=", text)
            if "<script" in text:
                scripted.append(page.relative_to(self.output).as_posix()); self.assertIn('<script src="/find.js" defer></script>', text)
        self.assertEqual(["find/index.html"], scripted)

    def test_build_does_not_modify_authoritative_objects(self):
        paths = list((build_site.ROOT / "objects").glob("*/*.json")); before = {path: path.read_bytes() for path in paths}; build_site.build(self.output); after = {path: path.read_bytes() for path in paths}; self.assertEqual(before, after)

    def test_build_refuses_to_replace_unmarked_directory(self):
        unknown = Path(self.tempdir.name) / "unknown"; unknown.mkdir(); (unknown / "keep.txt").write_text("do not delete", encoding="utf-8")
        with self.assertRaises(ValueError): build_site.build(unknown)
        self.assertEqual("do not delete", (unknown / "keep.txt").read_text(encoding="utf-8"))

    def test_source_links_allow_only_http_and_https(self):
        self.assertEqual("https://example.org/source", build_site.safe_http_url("https://example.org/source")); self.assertEqual("http://example.org/source", build_site.safe_http_url("http://example.org/source"))
        for value in ("javascript:alert(1)", "data:text/html,bad", "not-a-url"): self.assertIsNone(build_site.safe_http_url(value))


    def test_core_page_types_expose_semantic_identity(self):
        cases = [
            ("/", "page--home", ">ND Oracle</span>"),
            ("/find/", "page--find", ">Find</span>"),
            ("/questions/workplace-support-great-britain/", "page--question", ">Question</span>"),
            ("/resources/goblin-tools/", "page--resource", ">Resource</span>"),
            ("/understand/autism/", "page--concept", ">Concept</span>"),
            ("/evidence/", "page--evidence", ">Evidence</span>"),
        ]
        for route, body_class, label in cases:
            page = self.page(route)
            self.assertIn(body_class, page, route)
            self.assertIn('class="page-kind"', page, route)
            self.assertIn(label, page, route)

    def test_find_is_primary_navigation_and_has_accessible_local_controls(self):
        page = self.page("/find/")
        self.assertIn('href="/find/" aria-current="page">Find</a>', page)
        self.assertIn('aria-describedby="find-help"', page)
        self.assertIn('role="region" aria-label="Find results"', page)
        self.assertIn("Local governed discovery.", page)
        self.assertIn("processed only in this page", page)
        self.assertIn('<script src="/find.js" defer></script>', page)
        find_js = (self.output / "find.js").read_text(encoding="utf-8")
        self.assertIn("recordsByRoute", find_js)
        self.assertIn("record.scope.join", find_js)
        self.assertIn('scope.className = "scope-badge"', find_js)

    def test_jurisdiction_scope_is_visible_before_actionable_content(self):
        question = self.page("/questions/workplace-support-great-britain/")
        self.assertIn('class="scope-panel"', question)
        self.assertIn('class="scope-badge">Great Britain</span>', question)
        self.assertLess(question.index("Scope before you act"), question.index("Current understanding"))
        self.assertIn("not an eligibility, legal or clinical determination", question)

        scoped_resources = []
        for resource in self.resources:
            page = self.page(f'/resources/{resource["id"]}/')
            if 'class="scope-panel"' in page and 'International / not jurisdiction-specific' not in page:
                scoped_resources.append((resource, page))
        self.assertTrue(scoped_resources)
        resource, page = scoped_resources[0]
        self.assertLess(page.index("Scope for navigation"), page.index("What it is for"), resource["id"])
        self.assertIn("not an eligibility, legal or clinical determination", page)

    def test_visual_system_keeps_focus_touch_reduced_motion_and_forced_colors_explicit(self):
        css = (self.output / "styles.css").read_text(encoding="utf-8")
        for marker in (
            "--scope:",
            "--boundary:",
            ".page-kind",
            ".scope-panel",
            ".boundary-panel",
            "min-height: 2.75rem",
            'input[type="search"]',
            "@media (prefers-reduced-motion: no-preference)",
            "@media (forced-colors: active)",
        ):
            self.assertIn(marker, css)
        self.assertIn(":focus-visible", css)
        self.assertNotIn("@keyframes", css)

    def test_footer_exposes_evidence_governance_route(self):
        page = self.page("/")
        self.assertIn('aria-label="Footer"', page)
        self.assertIn('href="/evidence/">Evidence</a>', page)
        self.assertIn('href="/privacy/">Privacy</a>', page)


if __name__ == "__main__":
    unittest.main()
