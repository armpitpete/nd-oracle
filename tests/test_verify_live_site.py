from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "verify_live_site.py"
SPEC = importlib.util.spec_from_file_location("verify_live_site", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
verify_live_site = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verify_live_site
SPEC.loader.exec_module(verify_live_site)


class VerifyLiveSiteTests(unittest.TestCase):
    def response(
        self,
        *,
        status=200,
        final_url="https://ndoracle.org/",
        content_type="text/html; charset=utf-8",
        body="",
        headers=None,
    ):
        return verify_live_site.Response(
            status=status,
            final_url=final_url,
            content_type=content_type,
            body=body,
            headers=dict(verify_live_site.SECURITY_HEADERS if headers is None else headers),
        )

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

    def test_expected_legacy_route_set_is_complete(self):
        self.assertEqual(
            verify_live_site.LEGACY_ROUTES,
            ("/tools/", "/games/", "/resources/", "/community/", "/oracle/"),
        )

    def test_route_passes_with_exact_identity_security_and_passive_surface(self):
        origin = "https://ndoracle.org"
        path = "/about/"
        marker = "<h1>About</h1>"
        url = origin + path
        body = (
            f"{marker}\n{verify_live_site.canonical_marker(url)}"
            '<link rel="stylesheet" href="/styles.css">'
        )

        def fetcher(requested_url):
            self.assertEqual(requested_url, url)
            return self.response(final_url=url, body=body)

        self.assertEqual(
            verify_live_site.verify_route(origin, path, marker, fetcher=fetcher),
            [],
        )

    def test_route_rejects_identity_and_security_failures(self):
        def fetcher(_requested_url):
            return self.response(
                status=302,
                final_url="https://example.invalid/",
                content_type="text/plain",
                body="not the expected page",
                headers={},
            )

        failures = verify_live_site.verify_route(
            "https://ndoracle.org",
            "/privacy/",
            "<h1>Privacy</h1>",
            fetcher=fetcher,
        )
        self.assertTrue(any("HTTP 200" in failure for failure in failures))
        self.assertTrue(any("unexpected final URL" in failure for failure in failures))
        self.assertTrue(any("text/html" in failure for failure in failures))
        self.assertTrue(any("page marker" in failure for failure in failures))
        self.assertTrue(any("canonical link" in failure for failure in failures))
        self.assertTrue(any("missing security header" in failure for failure in failures))

    def test_security_headers_ignore_whitespace_only_differences(self):
        headers = dict(verify_live_site.SECURITY_HEADERS)
        headers["permissions-policy"] = "  accelerometer=(),   camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()  "
        response = self.response(headers=headers)
        self.assertEqual(verify_live_site.verify_security_headers("/", response), [])

    def test_passive_surface_rejects_collection_execution_and_external_loads(self):
        body = (
            '<form action="/submit"></form>'
            '<script src="/app.js"></script>'
            '<iframe src="https://example.invalid/frame"></iframe>'
            '<img src="https://tracker.invalid/pixel.gif">'
        )
        response = self.response(body=body)
        failures = verify_live_site.verify_passive_surface(
            "https://ndoracle.org", "/", response
        )
        self.assertTrue(any("form" in failure for failure in failures))
        self.assertTrue(any("script" in failure for failure in failures))
        self.assertTrue(any("iframe" in failure for failure in failures))
        self.assertTrue(any("externally loaded resource" in failure for failure in failures))

    def test_not_found_requires_real_404_noindex_and_security(self):
        origin = "https://ndoracle.org"
        url = origin + verify_live_site.NOT_FOUND_PATH
        body = f"{verify_live_site.NOT_FOUND_MARKER}{verify_live_site.NOINDEX_MARKER}"
        self.assertEqual(
            verify_live_site.verify_not_found(
                origin,
                fetcher=lambda requested: self.response(
                    status=404,
                    final_url=requested,
                    body=body,
                ),
            ),
            [],
        )
        self.assertEqual(url, origin + verify_live_site.NOT_FOUND_PATH)

    def test_legacy_routes_require_noindex(self):
        origin = "https://ndoracle.org"

        def fetcher(url):
            return self.response(final_url=url, body=verify_live_site.NOINDEX_MARKER)

        self.assertEqual(
            verify_live_site.verify_legacy_routes(origin, fetcher=fetcher),
            [],
        )

    def test_metadata_files_require_exact_public_index_set(self):
        origin = "https://ndoracle.org"
        sitemap_urls = "".join(
            f"<url><loc>{url}</loc></url>"
            for url in sorted(verify_live_site.expected_sitemap_urls(origin))
        )
        sitemap = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{sitemap_urls}</urlset>"
        )
        robots = verify_live_site.expected_origin_robots(origin)

        def fetcher(url):
            if url.endswith("/robots.txt"):
                return self.response(
                    final_url=url,
                    content_type="text/plain; charset=utf-8",
                    body=robots,
                )
            if url.endswith("/sitemap.xml"):
                return self.response(
                    final_url=url,
                    content_type="application/xml",
                    body=sitemap,
                )
            raise AssertionError(url)

        self.assertEqual(
            verify_live_site.verify_metadata_files(origin, fetcher=fetcher),
            [],
        )
        for legacy in verify_live_site.LEGACY_ROUTES:
            self.assertNotIn(origin + legacy, verify_live_site.expected_sitemap_urls(origin))

    def test_managed_robots_prefix_preserves_origin_contract(self):
        origin = "https://ndoracle.org"
        managed = (
            f"{verify_live_site.CLOUDFLARE_MANAGED_BEGIN}\n"
            f"{verify_live_site.CLOUDFLARE_CONTENT_SIGNAL}\n"
            "User-agent: GPTBot\nDisallow: /\n"
            f"{verify_live_site.CLOUDFLARE_MANAGED_END}\n\n"
            f"{verify_live_site.expected_origin_robots(origin)}"
        )
        self.assertEqual(verify_live_site.verify_robots_content(origin, managed), [])

    def test_managed_robots_rejects_changed_content_signal(self):
        origin = "https://ndoracle.org"
        managed = (
            f"{verify_live_site.CLOUDFLARE_MANAGED_BEGIN}\n"
            "Content-Signal: search=no,ai-train=yes,use=full\n"
            f"{verify_live_site.CLOUDFLARE_MANAGED_END}\n\n"
            f"{verify_live_site.expected_origin_robots(origin)}"
        )
        failures = verify_live_site.verify_robots_content(origin, managed)
        self.assertTrue(any("content signal changed" in failure for failure in failures))

    def test_sitemap_rejects_unexpected_legacy_route(self):
        origin = "https://ndoracle.org"
        sitemap = (
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f'<url><loc>{origin}/tools/</loc></url>'
            "</urlset>"
        )
        robots = verify_live_site.expected_origin_robots(origin)

        def fetcher(url):
            if url.endswith("robots.txt"):
                return self.response(final_url=url, body=robots)
            return self.response(final_url=url, body=sitemap)

        failures = verify_live_site.verify_metadata_files(origin, fetcher=fetcher)
        self.assertTrue(any("URL set mismatch" in failure for failure in failures))

    def test_www_redirect_requires_scheme_upgrade_apex_path_and_query(self):
        origin = "https://ndoracle.org"
        target = origin + "/understand/?q=nd-oracle-live-verify"
        seen = []

        def fetcher(url):
            seen.append(url)
            return self.response(
                final_url=target,
                body="<h1>Understand</h1>",
            )

        self.assertEqual(
            verify_live_site.verify_www_redirect(origin, fetcher=fetcher),
            [],
        )
        self.assertEqual(
            seen,
            [
                "http://www.ndoracle.org/understand/?q=nd-oracle-live-verify",
                "https://www.ndoracle.org/understand/?q=nd-oracle-live-verify",
            ],
        )

    def test_non_https_origin_is_refused(self):
        self.assertEqual(
            verify_live_site.main(["--origin", "http://ndoracle.org"]),
            2,
        )


if __name__ == "__main__":
    unittest.main()
