from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-cloudflare-pages.yml"
CHECKOUT_V7_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"


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

    def test_exact_release_sha_and_preexisting_protected_environment_are_required(self):
        for value in ("release_sha:", "required: true", "type: string", "^[0-9a-f]{40}$", "refs/heads/main", "actions: read", "/environments/{encoded_environment}", "cloudflare-pages-production must exist before dispatch", "refusing GitHub's implicit environment auto-creation path"):
            self.assertIn(value, self.text)
        self.assertGreaterEqual(self.text.count("/commits/main"), 2)
        self.assertIn('policy.get("protected_branches") is not True', self.text)
        self.assertIn('policy.get("custom_branch_policies") is not False', self.text)
        self.assertIn('rule.get("type") == "branch_policy"', self.text)

    def test_actions_and_wrangler_are_pinned(self):
        self.assertIn(f"actions/checkout@{CHECKOUT_V7_SHA}", self.text)
        self.assertIn("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", self.text)
        self.assertIn("actions/setup-node@820762786026740c76f36085b0efc47a31fe5020", self.text)
        self.assertIn("wrangler@4.114.0", self.text)
        self.assertNotIn("npx wrangler pages", self.text)

    def test_workflow_rebuilds_validates_and_keeps_static_runtime_fail_closed(self):
        for value in ("python scripts/validate.py", "python -m unittest discover -s tests", "python scripts/build_site.py", "test -f dist/index.html", "test -f dist/_headers", "Refusing deployment artifact containing symbolic links", "--experimental-provision=false", "--experimental-auto-create=false", "--install-skills=false"):
            self.assertIn(value, self.text)
        for forbidden in ("functions", "dist/_worker.js", "wrangler.toml", "wrangler.json", "wrangler.jsonc"):
            self.assertIn(forbidden, self.text)

    def test_cloudflare_identity_secrets_and_direct_upload_project_are_guarded(self):
        for value in ("secrets.CLOUDFLARE_API_TOKEN", "secrets.CLOUDFLARE_ACCOUNT_ID", "cloudflare-pages-production", "pages/projects/$PROJECT_NAME", "Expected existing Cloudflare Pages project nd-oracle", "Direct Upload project required"):
            self.assertIn(value, self.text)
        self.assertNotIn("pages project create", self.text)

    def test_deploy_command_preserves_exact_release_identity(self):
        for value in ("pages deploy dist", '--project-name="$PROJECT_NAME"', "--branch=main", '--commit-hash="$RELEASE_SHA"', "--commit-dirty=false"):
            self.assertIn(value, self.text)

    def test_accepted_pages_subdomain_and_custom_domain_set_are_required_without_mutation(self):
        self.assertGreaterEqual(self.text.count('expected_subdomain = "nd-oracle.pages.dev"'), 2)
        self.assertGreaterEqual(self.text.count('expected_custom_domains = {"ndoracle.org"}'), 2)
        self.assertGreaterEqual(self.text.count("custom_domains = domains - {subdomain}"), 2)
        self.assertGreaterEqual(self.text.count("if custom_domains != expected_custom_domains:"), 2)
        for value in ("Cloudflare Pages subdomain mismatch", "Cloudflare Pages subdomain changed before deployment", "Cloudflare Pages custom-domain set mismatch", "Cloudflare Pages custom-domain set changed before deployment", "missing = sorted(expected_custom_domains - custom_domains)", "unexpected = sorted(custom_domains - expected_custom_domains)", "no custom-domain or DNS mutation was requested"):
            self.assertIn(value, self.text)
        self.assertNotIn("Refusing deployment while ndoracle.org is attached", self.text)
        self.assertNotIn("ndoracle.org became attached before deployment", self.text)
        self.assertNotIn("pages domain", self.text)
        self.assertNotIn("dns record", self.text.lower())


if __name__ == "__main__":
    unittest.main()
