from __future__ import annotations

import unittest

from scripts import build_site, verify_live_site


class VerifyLiveSiteV10Tests(unittest.TestCase):
    def response(self, *, url="https://ndoracle.org/", body="", status=200, content_type="text/html; charset=utf-8", headers=None):
        return verify_live_site.Response(status, url, content_type, body, dict(verify_live_site.SECURITY_HEADERS if headers is None else headers))

    def test_current_route_set_exactly_matches_builder(self):
        paths = build_site.sitemap_paths(build_site.load_concepts(), build_site.load_resources(), build_site.load_questions())
        verifier_paths = [path for path, _marker in verify_live_site.V10_ROUTES]
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(paths))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), set(verifier_paths))
        self.assertEqual(len(verifier_paths), len(set(verifier_paths)))

    def test_frozen_compatibility_fixture_is_satisfied_by_current_corpus(self):
        self.assertEqual([], verify_live_site.verify_compatibility_fixture())

    def test_security_header_contract_allows_only_same_origin_script_execution(self):
        csp = verify_live_site.SECURITY_HEADERS["content-security-policy"]
        self.assertIn("script-src 'self'", csp)
        self.assertIn("connect-src 'none'", csp)
        self.assertIn("form-action 'none'", csp)
        self.assertIn("object-src 'none'", csp)
        self.assertNotIn("unsafe-inline", csp)
        self.assertNotIn("unsafe-eval", csp)

    def test_passive_surface_allows_exactly_find_js_on_find_page(self):
        find = self.response(url="https://ndoracle.org/find/", body='<main></main><script src="/find.js" defer></script>')
        self.assertEqual([], verify_live_site.verify_passive_surface("https://ndoracle.org", "/find/", find))
        normal = self.response(url="https://ndoracle.org/about/", body='<main></main><script src="/find.js"></script>')
        failures = verify_live_site.verify_passive_surface("https://ndoracle.org", "/about/", normal)
        self.assertTrue(any("unexpected script" in failure for failure in failures))

    def test_passive_surface_rejects_forms_iframes_and_external_loaded_resources(self):
        response = self.response(body='<form></form><iframe src="https://example.org/frame"></iframe><script src="https://example.org/a.js"></script>')
        failures = verify_live_site.verify_passive_surface("https://ndoracle.org", "/about/", response)
        self.assertTrue(any("form" in failure for failure in failures))
        self.assertTrue(any("iframe" in failure for failure in failures))
        self.assertTrue(any("externally loaded resource" in failure for failure in failures))

    def test_route_verifier_rejects_missing_canonical_and_security_header(self):
        url = "https://ndoracle.org/about/"
        response = self.response(url=url, body="<h1>About</h1>", headers={})
        failures = verify_live_site.verify_route("https://ndoracle.org", "/about/", "<h1>About</h1>", fetcher=lambda _url: response)
        self.assertTrue(any("canonical" in failure for failure in failures))
        self.assertTrue(any("missing security header" in failure for failure in failures))

    def test_robots_content_accepts_origin_block_and_rejects_changed_cloudflare_signal(self):
        origin = "https://ndoracle.org"
        base = verify_live_site.expected_origin_robots(origin)
        self.assertEqual([], verify_live_site.verify_robots_content(origin, base))
        managed = f"{verify_live_site.CLOUDFLARE_MANAGED_BEGIN}\nContent-Signal: search=no,ai-train=yes,use=reference\n{verify_live_site.CLOUDFLARE_MANAGED_END}\n{base}"
        failures = verify_live_site.verify_robots_content(origin, managed)
        self.assertTrue(any("content signal changed" in failure for failure in failures))

    def test_noindex_compatibility_route_remains_separate_from_canonical_routes(self):
        self.assertEqual(("/oracle/",), verify_live_site.COMPATIBILITY_NOINDEX_ROUTES)
        self.assertNotIn("/oracle/", {path for path, _marker in verify_live_site.V10_ROUTES})

    def test_non_https_origin_is_refused_before_network(self):
        self.assertEqual(2, verify_live_site.main(["--origin", "http://ndoracle.org"]))


if __name__ == "__main__":
    unittest.main()
