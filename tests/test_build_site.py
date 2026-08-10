import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_site


class WebsiteBuildTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)
        self.concepts = build_site.load_concepts()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_build_emits_index_and_every_concept(self):
        self.assertTrue((self.output / "index.html").is_file())
        self.assertTrue((self.output / "styles.css").is_file())
        for concept in self.concepts:
            self.assertTrue((self.output / "concepts" / f"{concept['id']}.html").is_file())

    def test_index_is_reading_first_and_non_clinical(self):
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("reading-first", page)
        self.assertIn("not diagnosis or medical advice", page)
        for concept in self.concepts:
            self.assertIn(concept["name"], page)
            self.assertIn(f"concepts/{concept['id']}.html", page)

    def test_every_claim_keeps_visible_evidence_and_uncertainty_routes(self):
        for concept in self.concepts:
            page = (self.output / "concepts" / f"{concept['id']}.html").read_text(encoding="utf-8")
            for claim in concept["claims"]:
                self.assertIn(claim["text"], page)
                for source_id in claim["source_ids"]:
                    self.assertIn(f'href="#source-{source_id}"', page)
                for uncertainty_id in claim["uncertainty_ids"]:
                    self.assertIn(f'href="#uncertainty-{uncertainty_id}"', page)

    def test_authoritative_objects_are_not_modified_by_build(self):
        before = {
            path: path.read_bytes()
            for path in build_site.OBJECTS_DIR.glob("*.json")
        }
        build_site.build(self.output)
        after = {path: path.read_bytes() for path in before}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
