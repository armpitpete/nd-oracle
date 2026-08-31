from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_BUILDERS = {"build_site_v06", "build_site_v08", "build_site_v09"}


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module)
            modules.update(alias.name for alias in node.names)
    return modules


class CurrentBuilderArchitectureTests(unittest.TestCase):
    def test_current_builder_has_no_legacy_builder_module_dependency(self) -> None:
        imports = imported_modules(ROOT / "scripts" / "build_site.py")
        for legacy in LEGACY_BUILDERS:
            self.assertNotIn(legacy, imports)
            self.assertNotIn(f"scripts.{legacy}", imports)

    def test_current_verifier_depends_only_on_current_builder(self) -> None:
        imports = imported_modules(ROOT / "scripts" / "verify_live_site.py")
        self.assertIn("build_site", imports)
        for legacy in LEGACY_BUILDERS:
            self.assertNotIn(legacy, imports)
            self.assertNotIn(f"scripts.{legacy}", imports)

    def test_v09_standalone_builder_is_not_part_of_current_tree(self) -> None:
        self.assertFalse((ROOT / "scripts" / "build_site_v09.py").exists())

    def test_public_compatibility_is_recorded_as_data(self) -> None:
        fixture = ROOT / "contracts" / "public-compatibility-v1.json"
        self.assertTrue(fixture.is_file())
        text = fixture.read_text(encoding="utf-8")
        for version in ('"v06"', '"v07"', '"v08"', '"v09"'):
            self.assertIn(version, text)


if __name__ == "__main__":
    unittest.main()
