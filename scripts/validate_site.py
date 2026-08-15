#!/usr/bin/env python3
"""Validate the generated Taxon Translate website using only Python's stdlib."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


REQUIRED_ROUTES = (
    "index.html",
    "privacy/index.html",
    "support/index.html",
    "beta-testing/index.html",
)
REQUIRED_ANCHORS = {
    "support/index.html": {
        "apple-books-use-a-shortcut",
        "which-languages-can-i-add",
        "why-does-a-selectable-language-have-few-or-no-names",
        "name-not-available",
    }
}


class ReferenceOutsideBasePath(ValueError):
    """A root-relative URL points outside the configured project site."""


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.motion_demos: list[dict[str, str]] = []
        self.motion_fallbacks: list[dict[str, str]] = []
        self.motion_controls: list[dict[str, str]] = []
        self.open_figures: list[dict[str, int]] = []
        self.open_code_blocks = 0
        self.structure_errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "figure":
            self.open_figures.append({"demos": 0, "fallbacks": 0, "controls": 0})
        if tag in {"code", "pre"}:
            self.open_code_blocks += 1
        if values.get("id"):
            self.ids.add(values["id"])
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append((attribute, values[attribute]))
        if tag == "img":
            classes = set(values.get("class", "").split())
            if "motion-demo" in classes:
                self.motion_demos.append(values)
                if self.open_figures:
                    self.open_figures[-1]["demos"] += 1
                else:
                    self.structure_errors.append("motion demo must be inside a figure")
            if "motion-fallback" in classes:
                self.motion_fallbacks.append(values)
                if self.open_figures:
                    self.open_figures[-1]["fallbacks"] += 1
                else:
                    self.structure_errors.append("motion fallback must be inside a figure")
        if tag == "button" and "motion-control" in set(values.get("class", "").split()):
            self.motion_controls.append(values)
            if self.open_figures:
                self.open_figures[-1]["controls"] += 1
            else:
                self.structure_errors.append("motion control must be inside a figure")

    def handle_endtag(self, tag: str) -> None:
        if tag == "figure" and self.open_figures:
            group = self.open_figures.pop()
            if any(group.values()) and group != {"demos": 1, "fallbacks": 1, "controls": 1}:
                self.structure_errors.append(
                    "motion figure must contain one demo, one fallback, and one control"
                )
        if tag in {"code", "pre"} and self.open_code_blocks:
            self.open_code_blocks -= 1

    def handle_data(self, data: str) -> None:
        if self.open_code_blocks and any(
            marker in data for marker in ("</article>", "</div>", "</section>")
        ):
            self.structure_errors.append("structural closing tag rendered as code")


def output_path_for_reference(
    site: Path, page: Path, reference: str, base_path: str = ""
) -> tuple[Path, str]:
    parsed = urlsplit(reference)
    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)
    if raw_path.startswith("/"):
        normalized_base_path = "/" + base_path.strip("/") if base_path.strip("/") else ""
        if normalized_base_path:
            if not (
                raw_path == normalized_base_path
                or raw_path.startswith(f"{normalized_base_path}/")
            ):
                raise ReferenceOutsideBasePath(reference)
            raw_path = raw_path[len(normalized_base_path) :] or "/"
        candidate = site / raw_path.lstrip("/")
    elif raw_path:
        candidate = page.parent / raw_path
    else:
        candidate = page
    candidate = candidate.resolve()
    if raw_path.endswith("/") or candidate.is_dir():
        candidate /= "index.html"
    return candidate, fragment


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def validate(site: Path, base_path: str = "") -> list[str]:
    site = site.resolve()
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}

    for route in REQUIRED_ROUTES:
        page = site / route
        if not page.is_file():
            errors.append(f"missing required route: {route}")

    for page in sorted(site.rglob("*.html")):
        try:
            pages[page] = parse_page(page)
        except (OSError, UnicodeError) as error:
            errors.append(f"cannot parse {page.relative_to(site)}: {error}")

    for route, anchors in REQUIRED_ANCHORS.items():
        page = site / route
        if page in pages:
            for anchor in sorted(anchors - pages[page].ids):
                errors.append(f"missing stable anchor in {route}: #{anchor}")

    ignored_schemes = {"http", "https", "mailto", "tel", "data"}
    for page, parser in list(pages.items()):
        route = page.relative_to(site)
        for error in parser.structure_errors:
            errors.append(f"{route}: invalid document structure: {error}")
        for attribute, reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme.lower() in ignored_schemes or reference.startswith("//"):
                continue
            try:
                target, fragment = output_path_for_reference(site, page, reference, base_path)
            except ReferenceOutsideBasePath:
                errors.append(
                    f"{route}: {attribute} points outside configured base path: {reference}"
                )
                continue
            try:
                target.relative_to(site)
            except ValueError:
                errors.append(f"{route}: {attribute} escapes generated site: {reference}")
                continue
            if not target.is_file():
                errors.append(f"{route}: broken internal {attribute}: {reference}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = pages.get(target)
                if target_parser is None:
                    target_parser = parse_page(target)
                    pages[target] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(f"{route}: missing link target: {reference}")

        for kind, images in (("demo", parser.motion_demos), ("fallback", parser.motion_fallbacks)):
            for image in images:
                if not image.get("alt", "").strip():
                    errors.append(f"{route}: motion {kind} requires meaningful alt text")
        for image in parser.motion_demos:
            if not urlsplit(image.get("src", "")).path.lower().endswith(".gif"):
                errors.append(f"{route}: motion demo must use a GIF: {image.get('src', '')}")
        for image in parser.motion_fallbacks:
            if urlsplit(image.get("src", "")).path.lower().endswith(".gif"):
                errors.append(f"{route}: motion fallback must be a still image: {image.get('src', '')}")

    css = site / "assets/site.css"
    if not css.is_file():
        errors.append("missing generated stylesheet: assets/site.css")
    else:
        styles = css.read_text(encoding="utf-8")
        for token in ("prefers-reduced-motion", ".motion-demo", ".motion-fallback"):
            if token not in styles:
                errors.append(f"stylesheet lacks reduced-motion requirement: {token}")

    return errors


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("site", type=Path, help="generated Jekyll output directory")
    argument_parser.add_argument(
        "--base-path",
        default="",
        help="URL path prefix used by GitHub Pages, such as /taxon-site",
    )
    arguments = argument_parser.parse_args()
    site = arguments.site.resolve()
    if not site.is_dir():
        argument_parser.error(f"generated site directory does not exist: {site}")

    errors = validate(site, arguments.base_path)
    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Website validation passed: {site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
