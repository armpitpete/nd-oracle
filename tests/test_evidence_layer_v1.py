from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery


class EvidenceLayerV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "dist"
        build_site.build(cls.output)
        cls.evidence_dirs = sorted(
            path for path in (cls.output / "evidence").iterdir() if path.is_dir()
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def page(self, route: str) -> str:
        path = self.output / route.strip("/") / "index.html"
        self.assertTrue(path.is_file(), route)
        return path.read_text(encoding="utf-8")

    def test_sixty_source_detail_routes_plus_index_remain_exact_in_current_contract(self) -> None:
        self.assertEqual(60, len(self.evidence_dirs))
        paths = build_site.sitemap_paths(build_site.load_concepts(), build_site.load_resources(), build_site.load_questions())
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(paths))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("/evidence/", paths)
        self.assertEqual(61, len([path for path in paths if path.startswith("/evidence/")]))

    def test_evidence_index_is_no_script_no_form_and_supports_browser_native_find(self) -> None:
        page = self.page("/evidence/")
        self.assertIn("<h1>Evidence</h1>", page)
        self.assertIn("Find in page", page)
        self.assertIn("Ctrl+F", page)
        self.assertNotIn("<script", page)
        self.assertNotIn("<form", page)
        self.assertFalse((self.output / "evidence-find.js").exists())

    def test_normalized_projection_exposes_claim_specific_evidence_fields(self) -> None:
        page = self.page("/evidence/acas-reasonable-adjustments-2025/")
        for marker in ("Finding used here:", "Population/context:", "Method:", "Evidence limitations"):
            self.assertIn(marker, page)
        self.assertIn("/resources/acas-reasonable-adjustments/", page)

    def test_legacy_projection_refuses_to_infer_v02_role(self) -> None:
        legacy = next(path for path in self.evidence_dirs if path.name.startswith("legacy-"))
        page = legacy.joinpath("index.html").read_text(encoding="utf-8")
        self.assertIn("legacy", page.lower())
        self.assertTrue("not" in page.lower() and "role" in page.lower())
        self.assertIn("/understand/", page)

    def test_ordinary_find_index_remains_free_of_evidence_routes(self) -> None:
        routes = {record["route"] for record in discovery.build_index()}
        self.assertFalse(any(route.startswith("/evidence/") for route in routes))

    def test_live_markers_cover_index_and_all_sixty_details(self) -> None:
        markers = build_site.evidence_route_markers()
        self.assertEqual(61, len(markers))
        self.assertEqual(61, len({path for path, _ in markers}))
        self.assertEqual("/evidence/", markers[0][0])


if __name__ == "__main__":
    unittest.main()
