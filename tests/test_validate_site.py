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
        (self.site / "beta-testing").mkdir()
        (self.site / "assets").mkdir()
        (self.site / "index.html").write_text(
            '<main id="main"><a href="support/#which-languages-can-i-add">FAQ</a><figure>'
            '<img class="motion-demo" src="assets/demo.gif" alt="Animated steps">'
            '<img class="motion-fallback" src="assets/poster.webp" alt="Still result">'
            '<button class="motion-control">Play animation</button></figure></main>',
            encoding="utf-8",
        )
        (self.site / "privacy/index.html").write_text('<main id="main"></main>', encoding="utf-8")
        (self.site / "support/index.html").write_text(
            f'<main id="main">{SUPPORT_ANCHORS}</main>', encoding="utf-8"
        )
        (self.site / "beta-testing/index.html").write_text(
            '<main id="main"></main>', encoding="utf-8"
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

    def test_accepts_absolute_links_with_project_site_base_path(self) -> None:
        (self.site / "index.html").write_text(
            '<main id="main"><a href="/taxon-site/support/#which-languages-can-i-add">FAQ</a><figure>'
            '<img class="motion-demo" src="/taxon-site/assets/demo.gif" alt="Animated steps">'
            '<img class="motion-fallback" src="/taxon-site/assets/poster.webp" alt="Still result">'
            '<button class="motion-control">Play animation</button></figure></main>',
            encoding="utf-8",
        )

        self.assertEqual(validate(self.site, "/taxon-site"), [])

    def test_rejects_absolute_links_outside_project_site_base_path(self) -> None:
        (self.site / "index.html").write_text(
            '<main id="main"><a href="/support/#which-languages-can-i-add">FAQ</a><figure>'
            '<img class="motion-demo" src="/assets/demo.gif" alt="Animated steps">'
            '<img class="motion-fallback" src="/assets/poster.webp" alt="Still result">'
            '<button class="motion-control">Play animation</button></figure></main>',
            encoding="utf-8",
        )

        errors = validate(self.site, "/taxon-site")

        self.assertEqual(len(errors), 3)
        self.assertTrue(all("outside configured base path" in error for error in errors))

    def test_reports_broken_contract_and_accessibility(self) -> None:
        (self.site / "support/index.html").write_text('<main id="main"></main>', encoding="utf-8")
        (self.site / "assets/poster.webp").unlink()

        errors = validate(self.site)

        self.assertTrue(any("missing stable anchor" in error for error in errors))
        self.assertTrue(any("broken internal src" in error for error in errors))

    def test_rejects_motion_without_replay_control(self) -> None:
        homepage = self.site / "index.html"
        homepage.write_text(
            homepage.read_text(encoding="utf-8").replace(
                '<button class="motion-control">Play animation</button>', ""
            ),
            encoding="utf-8",
        )

        errors = validate(self.site)

        self.assertTrue(any("motion figure must contain" in error for error in errors))

    def test_rejects_controls_paired_with_the_wrong_figure(self) -> None:
        homepage = self.site / "index.html"
        homepage.write_text(
            '<main><figure><img class="motion-demo" src="assets/demo.gif" alt="Animated steps">'
            '<img class="motion-fallback" src="assets/poster.webp" alt="Still result"></figure>'
            '<figure><button class="motion-control">Play</button>'
            '<button class="motion-control">Play again</button></figure></main>',
            encoding="utf-8",
        )

        errors = validate(self.site)

        self.assertEqual(sum("motion figure must contain" in error for error in errors), 2)

    def test_rejects_structural_closing_tag_rendered_as_code(self) -> None:
        homepage = self.site / "index.html"
        homepage.write_text(
            homepage.read_text(encoding="utf-8").replace(
                "</main>", "<pre><code>&lt;/section&gt;</code></pre></main>"
            ),
            encoding="utf-8",
        )

        errors = validate(self.site)

        self.assertTrue(any("structural closing tag rendered as code" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
