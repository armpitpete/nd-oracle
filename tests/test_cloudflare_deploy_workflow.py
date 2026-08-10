from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-cloudflare-pages.yml"


class CloudflareDeployWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_manual_only(self):
        self.assertIn("workflow_dispatch:", self.text)
        self.assertNotIn("\n  push:", self.text)
        self.assertNotIn("\n  pull_request:", self.text)
        self.assertNotIn("\n  schedule:", self.text)
        self.assertNotIn("workflow_call:", self.text)

    def test_exact_release_sha_is_required(self):
        self.assertIn("release_sha:", self.text)
        self.assertIn("required: true", self.text)
        self.assertIn("type: string", self.text)
        self.assertIn("^[0-9a-f]{40}$", self.text)
        self.assertIn("refs/heads/main", self.text)
        self.assertGreaterEqual(self.text.count("/commits/main"), 2)

    def test_actions_and_wrangler_are_pinned(self):
        self.assertIn(
            "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd",
            self.text,
        )
        self.assertIn(
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
            self.text,
        )
        self.assertIn(
            "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
            self.text,
        )
        self.assertIn("wrangler@4.114.0", self.text)
        self.assertNotIn("npx wrangler pages", self.text)

    def test_workflow_rebuilds_and_validates_dist(self):
        required = [
            "python scripts/validate.py",
            "python -m unittest discover -s tests",
            "python scripts/build_site.py",
            "test -f dist/index.html",
            "test -f dist/_headers",
            "Refusing deployment artifact containing symbolic links",
        ]
        for value in required:
            self.assertIn(value, self.text)

    def test_static_runtime_boundary_is_fail_closed(self):
        for forbidden in [
            "functions",
            "dist/_worker.js",
            "wrangler.toml",
            "wrangler.json",
            "wrangler.jsonc",
        ]:
            self.assertIn(forbidden, self.text)
        self.assertIn("--experimental-provision=false", self.text)
        self.assertIn("--experimental-auto-create=false", self.text)
        self.assertIn("--install-skills=false", self.text)

    def test_cloudflare_secrets_are_used_without_literal_credentials(self):
        self.assertIn("secrets.CLOUDFLARE_API_TOKEN", self.text)
        self.assertIn("secrets.CLOUDFLARE_ACCOUNT_ID", self.text)
        self.assertIn("cloudflare-pages-production", self.text)

    def test_existing_direct_upload_project_is_required(self):
        self.assertIn("pages/projects/$PROJECT_NAME", self.text)
        self.assertIn("Expected existing Cloudflare Pages project nd-oracle", self.text)
        self.assertIn("Direct Upload project required", self.text)
        self.assertNotIn("pages project create", self.text)

    def test_deploy_command_preserves_release_identity(self):
        self.assertIn("pages deploy dist", self.text)
        self.assertIn('--project-name="$PROJECT_NAME"', self.text)
        self.assertIn("--branch=main", self.text)
        self.assertIn('--commit-hash="$RELEASE_SHA"', self.text)
        self.assertIn("--commit-dirty=false", self.text)

    def test_domain_and_dns_boundary_is_explicit(self):
        self.assertIn("ndoracle.org became attached before deployment; refusing upload", self.text)
        self.assertIn("Custom-domain and DNS mutation: not requested by this workflow", self.text)
        self.assertNotIn("pages domain", self.text)
        self.assertNotIn("dns record", self.text.lower())


if __name__ == "__main__":
    unittest.main()
