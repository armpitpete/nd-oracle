from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts import build_site


BATCH_A_IDS = {
    "dyslexia",
    "developmental-coordination-disorder",
    "tourette-syndrome",
    "learning-disability",
    "developmental-language-disorder",
}


class BatchAPublicSiteTests(unittest.TestCase):
    def test_batch_a_routes_remain_present_as_topic_corpus_grows(self) -> None:
        concepts = build_site.load_concepts()
        ids = {concept["id"] for concept in concepts}
        self.assertTrue(BATCH_A_IDS.issubset(ids))
        self.assertGreaterEqual(len(concepts), 10)

        with tempfile.TemporaryDirectory() as tmp:
            output = build_site.build(Path(tmp) / "site")
            for object_id in BATCH_A_IDS:
                page = output / "understand" / object_id / "index.html"
                self.assertTrue(page.is_file(), object_id)
                text = page.read_text(encoding="utf-8")
                self.assertIn("What we can say", text, object_id)
                self.assertIn("What remains uncertain", text, object_id)
                self.assertIn("Sources", text, object_id)

            homepage = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn(f"{len(concepts)} evidence-linked topics are available now", homepage)
            self.assertNotIn("Five core topics", homepage)

            about = (output / "about" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("five core topics", about.casefold())

            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
            for object_id in BATCH_A_IDS:
                self.assertIn(f"https://ndoracle.org/understand/{object_id}/", sitemap)


if __name__ == "__main__":
    unittest.main()
