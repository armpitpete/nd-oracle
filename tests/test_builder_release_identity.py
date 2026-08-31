from __future__ import annotations

import unittest
from pathlib import Path

from scripts.release_identity import PUBLIC_SITE_RELEASE


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_site.py"
IDENTITY = ROOT / "scripts" / "release_identity.py"


class BuilderReleaseIdentityTests(unittest.TestCase):
    def test_public_site_release_identity_is_explicit_v11(self) -> None:
        self.assertEqual("v1.1", PUBLIC_SITE_RELEASE)
        self.assertTrue(IDENTITY.is_file())

    def test_builder_uses_identity_without_stale_hard_coded_label(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn("from scripts.release_identity import PUBLIC_SITE_RELEASE", text)
        self.assertIn("public site {PUBLIC_SITE_RELEASE}", text)
        self.assertNotIn("public site v1.0 candidate", text)

    def test_builder_monolith_was_not_truncated(self) -> None:
        self.assertGreater(BUILDER.stat().st_size, 100_000)


if __name__ == "__main__":
    unittest.main()
