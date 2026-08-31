from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery
from scripts.release_identity import PUBLIC_SITE_RELEASE

ROOT = Path(__file__).resolve().parents[1]


class TemporaryV12ReleasePreflight(unittest.TestCase):
    def test_emit_release_preflight(self) -> None:
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()
        self.assertEqual((20, 61, 41, 3), (len(concepts), len(resources), len(questions), len(evidence)))
        self.assertEqual(125, len(concepts) + len(resources) + len(questions) + len(evidence))
        self.assertEqual("v1.2", PUBLIC_SITE_RELEASE)
        self.assertEqual(148, build_site.V10_ROUTE_COUNT)
        self.assertEqual(148, len(build_site.sitemap_paths(concepts, resources, questions)))

        probes = {
            "disabled student support Scotland": "/questions/disabled-student-support-scotland/",
            "disabled student support Wales": "/questions/disabled-student-support-wales/",
            "disabled student support Northern Ireland": "/questions/disabled-student-support-northern-ireland/",
            "disabled student support England": "/questions/disabled-student-support-england/",
        }
        for query, expected in probes.items():
            trace, results = discovery.evaluate(query)
            self.assertEqual("results", trace["final_reason"])
            self.assertTrue(results)
            self.assertEqual(expected, results[0].route)

        with tempfile.TemporaryDirectory() as tempdir:
            dist = Path(tempdir) / "dist"
            destination = build_site.build(dist)
            self.assertEqual(dist, destination)
            self.assertTrue((dist / "index.html").is_file())
            self.assertTrue((dist / "styles.css").is_file())
            self.assertTrue((dist / "_headers").is_file())
            self.assertTrue((dist / ".nd-oracle-generated").is_file())
            self.assertFalse((dist / "_worker.js").exists())
            self.assertFalse(any(path.is_symlink() for path in dist.rglob("*")))

            digest = hashlib.sha256()
            files = sorted(path for path in dist.rglob("*") if path.is_file())
            for path in files:
                relative = path.relative_to(dist).as_posix().encode("utf-8")
                payload = path.read_bytes()
                digest.update(len(relative).to_bytes(8, "big"))
                digest.update(relative)
                digest.update(len(payload).to_bytes(8, "big"))
                digest.update(payload)
            report = {
                "artifact_sha256": digest.hexdigest(),
                "canonical_routes": len(build_site.sitemap_paths(concepts, resources, questions)),
                "counts": {"concepts": 20, "resources": 61, "questions": 41, "evidence": 3},
                "public_site_release": PUBLIC_SITE_RELEASE,
                "static_files": len(files),
            }
            print("V12_RELEASE_PREFLIGHT_JSON=" + json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
