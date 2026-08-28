from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_site, verify_live_site


EXPECTED_GROUPS = {
    "Daily life & technology": {
        "task-starting-and-organisation",
        "make-device-easier-to-use",
        "meal-planning-and-everyday-food-tasks",
    },
    "Sensory & environment": {
        "make-noisy-bright-place-easier",
        "sensory-overload-what-can-i-change",
    },
    "Communication": {
        "aac-and-nonspeaking-communication",
        "phone-calls-are-difficult",
        "processing-time-in-conversations-meetings",
    },
    "Work": {
        "workplace-support-great-britain",
        "reasonable-adjustments-at-work-great-britain",
        "disabled-person-looking-for-work-uk",
        "disclosing-disability-neurodivergence-at-work",
        "job-interview-adjustments-great-britain",
    },
    "Education & study": {
        "disabled-student-support-england",
        "organising-study-and-assignments",
        "send-support-school-college-england",
    },
    "Assessment & diagnosis": {
        "adult-adhd-assessment-england",
        "adult-autism-assessment-england",
    },
    "Health & wellbeing": {
        "autism-anxiety-tools",
        "masking-exhaustion-and-autistic-burnout",
        "sleep-and-winding-down-routines",
    },
    "Relationships & family": {"autistic-parent-support-uk"},
    "Information & support": {
        "autism-information-and-support",
        "dyslexia-information-and-support-uk",
        "tourette-information-and-support-uk",
        "learning-disability-information-and-support-uk",
        "dld-information-and-support",
        "adult-dyspraxia-information-uk",
        "dyscalculia-information-and-support-uk",
    },
    "Games & downtime": {"low-time-pressure-games"},
}


class ContentNavigationV09Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.concepts = build_site.load_concepts()
        self.resources = build_site.load_resources()
        self.questions = build_site.load_questions()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _page(self, route: str) -> str:
        if route == "/":
            target = self.output / "index.html"
        else:
            target = self.output / route.strip("/") / "index.html"
        self.assertTrue(target.is_file(), target)
        return target.read_text(encoding="utf-8")

    def test_v09_reaches_100_governed_objects(self) -> None:
        self.assertEqual(20, len(self.concepts))
        self.assertEqual(50, len(self.resources))
        self.assertEqual(30, len(self.questions))
        self.assertEqual(100, len(self.concepts) + len(self.resources) + len(self.questions))
        for resource in self.resources:
            self.assertEqual("reviewed", resource["status"])
            self.assertEqual([], resource["claims"])

    def test_question_groups_are_explicit_and_cover_every_question_once(self) -> None:
        build_site.validate_question_navigation(self.questions)
        actual = {group: set(ids) for group, ids in build_site.QUESTION_GROUPS}
        self.assertEqual(EXPECTED_GROUPS, actual)
        grouped = [question_id for _group, ids in build_site.QUESTION_GROUPS for question_id in ids]
        self.assertEqual(30, len(grouped))
        self.assertEqual(30, len(set(grouped)))
        self.assertEqual({item["id"] for item in self.questions}, set(grouped))

    def test_homepage_preserves_frozen_v07_question_routes(self) -> None:
        page = self._page("/")
        question_map = {item["id"]: item for item in self.questions}
        self.assertEqual(
            set(verify_live_site.V07_QUESTION_IDS),
            set(build_site.V07_HOMEPAGE_COMPAT_QUESTION_IDS),
        )
        for question_id in build_site.V07_HOMEPAGE_COMPAT_QUESTION_IDS:
            question = question_map[question_id]
            self.assertIn(f'href="/questions/{question_id}/"', page)
            self.assertIn(build_site.esc(question["question"]), page)

    def test_candidate_contract_is_exactly_125_routes(self) -> None:
        paths = build_site.sitemap_paths(self.concepts, self.resources, self.questions)
        self.assertEqual(125, len(paths))
        self.assertEqual(125, len(set(paths)))
        self.assertEqual(set(build_site.NAVIGATION_ROUTES), set(build_site.NAVIGATION_ROUTES) & set(paths))
        self.assertEqual(125, len(verify_live_site.V09_ROUTES))
        self.assertEqual(set(paths), {path for path, _marker in verify_live_site.V09_ROUTES})

    def test_needs_index_reaches_every_question(self) -> None:
        page = self._page("/needs/")
        self.assertIn("Start with the need, not the label.", page)
        for question in self.questions:
            self.assertIn(f'href="/questions/{question["id"]}/"', page)

    def test_eight_need_hubs_are_built_with_boundaries_and_content(self) -> None:
        self.assertEqual(8, len(build_site.HUB_DEFINITIONS))
        for route, title, _intro, groups in build_site.HUB_DEFINITIONS:
            page = self._page(f"/{route}/")
            self.assertIn(f"<h1>{build_site.esc(title)}</h1>", page)
            self.assertIn("Relevant to inspect, not recommended.", page)
            self.assertIn("Practical questions", page)
            expected_ids = {
                question_id
                for group, ids in build_site.QUESTION_GROUPS
                if group in groups
                for question_id in ids
            }
            self.assertTrue(expected_ids, route)
            for question_id in expected_ids:
                self.assertIn(f'href="/questions/{question_id}/"', page)

    def test_content_type_index_reaches_every_resource(self) -> None:
        page = self._page("/types/")
        self.assertIn("<h2>Questions</h2>", page)
        self.assertIn("<h2>Topics</h2>", page)
        for resource in self.resources:
            self.assertIn(f'href="/resources/{resource["id"]}/"', page)

    def test_geographic_index_reaches_every_resource(self) -> None:
        page = self._page("/places/")
        self.assertIn("Navigation scope, not eligibility.", page)
        for resource in self.resources:
            self.assertIn(f'href="/resources/{resource["id"]}/"', page)

    def test_az_reaches_all_100_governed_objects(self) -> None:
        page = self._page("/a-z/")
        self.assertIn("All 100 governed Topics, Resources and Questions", page)
        for concept in self.concepts:
            self.assertIn(f'href="/understand/{concept["id"]}/"', page)
        for resource in self.resources:
            self.assertIn(f'href="/resources/{resource["id"]}/"', page)
        for question in self.questions:
            self.assertIn(f'href="/questions/{question["id"]}/"', page)

    def test_question_pages_include_adjacent_question_navigation(self) -> None:
        for question in self.questions:
            page = self._page(f'/questions/{question["id"]}/')
            self.assertIn('<h2 id="related-questions-heading">Related questions</h2>', page)

    def test_resource_pages_include_scope_navigation(self) -> None:
        for resource in self.resources:
            page = self._page(f'/resources/{resource["id"]}/')
            self.assertIn('<h2 id="scope-heading">Scope for navigation</h2>', page)
            self.assertIn('href="/places/"', page)
            self.assertIn('href="/types/"', page)

    def test_v09_verifier_contracts_accept_actual_built_site(self) -> None:
        origin = "https://ndoracle.org"

        def fetcher(url: str):
            path = url.removeprefix(origin)
            if path == "/":
                target = self.output / "index.html"
            else:
                target = self.output / path.strip("/") / "index.html"
            self.assertTrue(target.is_file(), target)
            return verify_live_site.Response(
                status=200,
                final_url=url,
                content_type="text/html; charset=utf-8",
                body=target.read_text(encoding="utf-8"),
                headers=dict(verify_live_site.SECURITY_HEADERS),
            )

        self.assertEqual([], verify_live_site.verify_v08_subset_preserved())
        self.assertEqual([], verify_live_site.verify_v09_concept_contract(origin, fetcher=fetcher))
        self.assertEqual([], verify_live_site.verify_v09_question_contract(origin, fetcher=fetcher))
        self.assertEqual([], verify_live_site.verify_v09_resource_contract(origin, fetcher=fetcher))
        self.assertEqual([], verify_live_site.verify_v09_navigation_contract(origin, fetcher=fetcher))


if __name__ == "__main__":
    unittest.main()
