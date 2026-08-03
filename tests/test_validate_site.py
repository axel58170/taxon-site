import tempfile
import unittest
from pathlib import Path

from scripts.validate_site import validate


SUPPORT_ANCHORS = "".join(
    f'<h2 id="{anchor}"></h2>'
    for anchor in (
        "apple-books-use-a-shortcut",
        "which-languages-can-i-add",
        "why-does-a-selectable-language-have-few-or-no-names",
        "name-not-available",
    )
)


class GeneratedSiteValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.site = Path(self.temporary_directory.name)
        (self.site / "privacy").mkdir()
        (self.site / "support").mkdir()
        (self.site / "assets").mkdir()
        (self.site / "index.html").write_text(
            '<main id="main"><a href="support/#which-languages-can-i-add">FAQ</a>'
            '<img class="motion-demo" src="assets/demo.gif" alt="Animated steps">'
            '<img class="motion-fallback" src="assets/poster.webp" alt="Still result"></main>',
            encoding="utf-8",
        )
        (self.site / "privacy/index.html").write_text('<main id="main"></main>', encoding="utf-8")
        (self.site / "support/index.html").write_text(
            f'<main id="main">{SUPPORT_ANCHORS}</main>', encoding="utf-8"
        )
        (self.site / "assets/site.css").write_text(
            "@media (prefers-reduced-motion: reduce) {"
            ".motion-demo { display: none; } .motion-fallback { display: block; }}",
            encoding="utf-8",
        )
        (self.site / "assets/demo.gif").touch()
        (self.site / "assets/poster.webp").touch()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_accepts_complete_generated_site(self) -> None:
        self.assertEqual(validate(self.site), [])

    def test_reports_broken_contract_and_accessibility(self) -> None:
        (self.site / "support/index.html").write_text('<main id="main"></main>', encoding="utf-8")
        (self.site / "assets/poster.webp").unlink()

        errors = validate(self.site)

        self.assertTrue(any("missing stable anchor" in error for error in errors))
        self.assertTrue(any("broken internal src" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
