import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VercelConfigTests(unittest.TestCase):
    def test_configuration_is_minimal_static_build_only(self):
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(config),
            {"$schema", "buildCommand", "outputDirectory", "installCommand"},
        )
        self.assertEqual(config["$schema"], "https://openapi.vercel.sh/vercel.json")
        self.assertEqual(config["buildCommand"], "python scripts/build_site.py")
        self.assertEqual(config["outputDirectory"], "dist")
        self.assertEqual(config["installCommand"], "")

    def test_python_version_matches_repository_ci(self):
        self.assertEqual((ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13")


if __name__ == "__main__":
    unittest.main()
