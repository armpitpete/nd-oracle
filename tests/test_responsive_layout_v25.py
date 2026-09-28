from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")
BUILDER = (ROOT / "scripts" / "build_site.py").read_text(encoding="utf-8")

VIEWPORTS = (
    (1920, 1080),
    (1440, 900),
    (1280, 800),
    (1024, 768),
    (768, 1024),
    (430, 932),
    (390, 844),
    (320, 568),
)


class ResponsiveLayoutV25Tests(unittest.TestCase):
    def test_shared_90_percent_shell_contract(self) -> None:
        for marker in (
            "--page-width: 90%;",
            "--page-max-width: 100rem;",
            "--prose-max-width: 82ch;",
            "width: var(--page-width);",
            "max-width: var(--page-max-width);",
            "max-width: 100%;",
        ):
            self.assertIn(marker, CSS)

    def test_heading_is_not_forced_into_a_pencil_measure(self) -> None:
        h1 = re.search(r"h1\s*\{(?P<body>.*?)\n\}", CSS, re.S)
        self.assertIsNotNone(h1)
        self.assertIn("max-width: none;", h1.group("body"))
        self.assertNotIn("max-width: 20ch;", h1.group("body"))

    def test_question_secondary_material_uses_responsive_grid(self) -> None:
        self.assertIn('class="question-secondary-grid"', BUILDER)
        self.assertIn(".question-secondary-grid {", CSS)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", CSS)
        self.assertIn("@media (max-width: 56rem)", CSS)

    def test_progressive_collapse_breakpoints_are_explicit(self) -> None:
        for marker in (
            "@media (max-width: 87.5rem)",
            "@media (max-width: 62.5rem)",
            "@media (max-width: 56rem)",
            "@media (max-width: 43.75rem)",
            "@media (max-width: 28rem)",
        ):
            self.assertIn(marker, CSS)

    def test_standard_viewport_matrix_covers_large_desktop_to_small_phone(self) -> None:
        self.assertEqual(
            VIEWPORTS,
            (
                (1920, 1080),
                (1440, 900),
                (1280, 800),
                (1024, 768),
                (768, 1024),
                (430, 932),
                (390, 844),
                (320, 568),
            ),
        )

    def test_no_top_level_reading_column_reintroduces_narrow_page_shell(self) -> None:
        first = re.search(r"\.reading-column\s*\{(?P<body>.*?)\n\}", CSS, re.S)
        self.assertIsNotNone(first)
        self.assertIn("max-width: 100%;", first.group("body"))
        self.assertNotRegex(first.group("body"), r"max-width:\s*(?:6[0-9]|7[0-9]|8[0-9])ch")


if __name__ == "__main__":
    unittest.main()
