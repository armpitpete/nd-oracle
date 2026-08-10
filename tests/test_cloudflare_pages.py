import tempfile
import unittest
from pathlib import Path

from scripts import build_site


class CloudflarePagesHardeningTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.output = Path(self.tempdir.name) / "dist"
        build_site.build(self.output)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_security_headers_are_copied_verbatim_into_deployment(self):
        source = (build_site.SITE_DIR / "_headers").read_bytes()
        generated = (self.output / "_headers").read_bytes()
        self.assertEqual(generated, source)

    def test_security_policy_is_restrictive_for_static_site_with_bounded_analytics(self):
        headers = (self.output / "_headers").read_text(encoding="utf-8")
        required = [
            "default-src 'none'",
            "style-src 'self'",
            "script-src https://collect.merrinworld.uk",
            "connect-src https://collect.merrinworld.uk",
            "object-src 'none'",
            "base-uri 'none'",
            "form-action 'none'",
            "frame-ancestors 'none'",
            "Strict-Transport-Security: max-age=31536000",
            "Cross-Origin-Opener-Policy: same-origin",
            "Cross-Origin-Resource-Policy: same-origin",
            "X-Frame-Options: DENY",
            "X-Content-Type-Options: nosniff",
            "X-Permitted-Cross-Domain-Policies: none",
            "Referrer-Policy: no-referrer",
            "Permissions-Policy:",
        ]
        for value in required:
            self.assertIn(value, headers)
        self.assertNotIn("'unsafe-inline'", headers)
        self.assertNotIn("'unsafe-eval'", headers)
        self.assertNotIn("script-src 'self'", headers)
        self.assertNotIn("connect-src 'self'", headers)

    def test_generated_html_has_only_optional_analytics_javascript_and_no_forms(self):
        expected_script = (
            '<script src="https://collect.merrinworld.uk/beacon.js" '
            'data-site="nd_oracle" defer></script>'
        )
        for page in sorted(self.output.rglob("*.html")):
            text = page.read_text(encoding="utf-8")
            lower = text.lower()
            self.assertEqual(text.count(expected_script), 1)
            self.assertEqual(lower.count("<script"), 1)
            self.assertNotIn("<form", lower)
            self.assertNotIn("style=", lower)

    def test_privacy_page_discloses_visitor_estimation_boundary(self):
        privacy = (self.output / "privacy" / "index.html").read_text(encoding="utf-8")
        required = [
            "random site-local browser token",
            "no IP address",
            "raw visitor token",
            "cross-site visitor identity",
            "fully readable if the analytics script is blocked",
        ]
        for value in required:
            self.assertIn(value, privacy)

    def test_release_contract_requires_exact_commit_owner_gate_and_pinned_cli(self):
        notes = (build_site.SITE_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx --yes wrangler@4.114.0 pages deploy dist", notes)
        self.assertIn("--commit-hash=<EXACT_MAIN_SHA>", notes)
        self.assertIn("--commit-dirty=false", notes)
        self.assertIn("explicit owner authorisation", notes)
        self.assertIn("Custom-domain attachment and DNS changes are later protected actions", notes)
        self.assertNotIn("\nnpx wrangler pages deploy", notes)


if __name__ == "__main__":
    unittest.main()