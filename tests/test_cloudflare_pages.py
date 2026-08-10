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

    def test_security_policy_is_restrictive_for_current_static_site(self):
        headers = (self.output / "_headers").read_text(encoding="utf-8")
        required = [
            "default-src 'none'",
            "style-src 'self'",
            "script-src 'none'",
            "connect-src 'none'",
            "object-src 'none'",
            "base-uri 'none'",
            "form-action 'none'",
            "frame-ancestors 'none'",
            "X-Frame-Options: DENY",
            "X-Content-Type-Options: nosniff",
            "Referrer-Policy: no-referrer",
            "Permissions-Policy:",
        ]
        for value in required:
            self.assertIn(value, headers)
        self.assertNotIn("'unsafe-inline'", headers)
        self.assertNotIn("'unsafe-eval'", headers)

    def test_generated_html_matches_javascript_free_form_free_policy(self):
        pages = [self.output / "index.html", *sorted((self.output / "concepts").glob("*.html"))]
        for page in pages:
            text = page.read_text(encoding="utf-8").lower()
            self.assertNotIn("<script", text)
            self.assertNotIn("<form", text)
            self.assertNotIn("style=", text)

    def test_release_contract_requires_exact_commit_and_owner_gate(self):
        notes = (build_site.SITE_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("--commit-hash=<EXACT_MAIN_SHA>", notes)
        self.assertIn("--commit-dirty=false", notes)
        self.assertIn("explicit owner authorisation", notes)
        self.assertIn("Custom-domain attachment and DNS changes are later protected actions", notes)


if __name__ == "__main__":
    unittest.main()
