from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, verify_live_site

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "contracts" / "public-compatibility-v1.json").read_text(encoding="utf-8"))
V09 = FIXTURE["v09"]


class ContentNavigationV09CompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.concepts = build_site.load_concepts()
        self.resources = build_site.load_resources()
        self.questions = build_site.load_questions()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def page(self, route: str) -> str:
        target = self.output / "index.html" if route == "/" else self.output / route.strip("/") / "index.html"
        self.assertTrue(target.is_file(), target)
        return target.read_text(encoding="utf-8")

    def test_current_corpus_contains_at_least_the_frozen_v09_scale(self) -> None:
        counts = V09["counts"]
        self.assertGreaterEqual(len(self.concepts), counts["concepts"])
        self.assertGreaterEqual(len(self.resources), counts["resources"])
        self.assertGreaterEqual(len(self.questions), counts["questions"])
        self.assertGreaterEqual(len(self.concepts) + len(self.resources) + len(self.questions), counts["governed_objects"])

    def test_frozen_v09_question_groups_remain_present_as_subsets(self) -> None:
        current = {group: set(ids) for group, ids in build_site.QUESTION_GROUPS}
        for group, frozen_ids in V09["question_groups"].items():
            self.assertIn(group, current)
            self.assertTrue(set(frozen_ids) <= current[group], group)
        build_site.validate_question_navigation(self.questions)

    def test_frozen_v09_navigation_routes_remain_current(self) -> None:
        current_paths = set(build_site.sitemap_paths(self.concepts, self.resources, self.questions))
        self.assertTrue(set(V09["navigation_routes"]) <= current_paths)
        self.assertGreaterEqual(len(current_paths), V09["route_count"])

    def test_homepage_preserves_v07_question_routes(self) -> None:
        page = self.page("/")
        question_map = {item["id"]: item for item in self.questions}
        for question_id in FIXTURE["v07"]["question_ids"]:
            self.assertIn(question_id, question_map)
            self.assertIn(f'href="/questions/{question_id}/"', page)

    def test_current_needs_types_places_and_az_reach_the_current_corpus(self) -> None:
        needs = self.page("/needs/")
        types = self.page("/types/")
        places = self.page("/places/")
        az = self.page("/a-z/")
        for question in self.questions:
            self.assertIn(f'href="/questions/{question["id"]}/"', needs)
            self.assertIn(f'href="/questions/{question["id"]}/"', az)
        for concept in self.concepts:
            self.assertIn(f'href="/understand/{concept["id"]}/"', az)
        for resource in self.resources:
            route = f'/resources/{resource["id"]}/'
            self.assertIn(f'href="{route}"', types)
            self.assertIn(f'href="{route}"', places)
            self.assertIn(f'href="{route}"', az)

    def test_current_detail_navigation_contracts_are_present(self) -> None:
        for question in self.questions:
            page = self.page(f'/questions/{question["id"]}/')
            self.assertIn('<h2 id="related-questions-heading">Related questions</h2>', page)
        for resource in self.resources:
            page = self.page(f'/resources/{resource["id"]}/')
            self.assertIn('<h2 id="scope-heading">Scope for navigation</h2>', page)
            self.assertIn('href="/places/"', page)
            self.assertIn('href="/types/"', page)

    def test_frozen_compatibility_fixture_and_current_v1_contract_agree(self) -> None:
        self.assertEqual([], verify_live_site.verify_compatibility_fixture())
        paths = build_site.sitemap_paths(self.concepts, self.resources, self.questions)
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(paths))
        self.assertEqual(set(paths), {path for path, _marker in verify_live_site.V10_ROUTES})


if __name__ == "__main__":
    unittest.main()
