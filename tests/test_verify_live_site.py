from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "verify_live_site.py"
SPEC = importlib.util.spec_from_file_location("verify_live_site", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
verify_live_site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_live_site)


class VerifyLiveSiteTests(unittest.TestCase):
    def test_expected_canonical_route_set_is_complete(self):
        self.assertEqual(
            tuple(path for path, _ in verify_live_site.ROUTES),
            (
                "/",
                "/understand/",
                "/understand/neurodiversity/",
                "/understand/autism/",
                "/understand/adhd/",
                "/understand/executive-function/",
                "/understand/sensory-processing/",
                "/how-it-works/",
                "/about/",
                "/accessibility/",
                "/privacy/",
            ),
        )

    def test_route_passes_only_with_exact_url_html_marker_and_canonical(self):
        origin = "https://ndoracle.org"
        path = "/about/"
        marker = "<h1>About</h1>"
        url = origin + path

        def fetcher(requested_url):
            self.assertEqual(requested_url, url)
            return verify_live_site.Response(
                status=200,
                final_url=url,
                content_type="text/html; charset=utf-8",
                body=f"{marker}\n{verify_live_site.canonical_marker(url)}",
            )

        self.assertEqual(
            verify_live_site.verify_route(origin, path, marker, fetcher=fetcher),
            [],
        )

    def test_route_rejects_redirect_wrong_status_wrong_type_missing_content(self):
        def fetcher(_requested_url):
            return verify_live_site.Response(
                status=302,
                final_url="https://example.invalid/",
                content_type="text/plain",
                body="not the expected page",
            )

        failures = verify_live_site.verify_route(
            "https://ndoracle.org",
            "/privacy/",
            "<h1>Privacy</h1>",
            fetcher=fetcher,
        )
        self.assertEqual(len(failures), 5)
        self.assertTrue(any("HTTP 200" in failure for failure in failures))
        self.assertTrue(any("unexpected final URL" in failure for failure in failures))
        self.assertTrue(any("text/html" in failure for failure in failures))
        self.assertTrue(any("page marker" in failure for failure in failures))
        self.assertTrue(any("canonical link" in failure for failure in failures))

    def test_non_https_origin_is_refused(self):
        self.assertEqual(
            verify_live_site.main(["--origin", "http://ndoracle.org"]),
            2,
        )


if __name__ == "__main__":
    unittest.main()
