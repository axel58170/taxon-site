#!/usr/bin/env python3
"""Validate the generated Taxon Bridge website using only Python's stdlib."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


REQUIRED_ROUTES = ("index.html", "privacy/index.html", "support/index.html")
REQUIRED_ANCHORS = {
    "support/index.html": {
        "apple-books-use-a-shortcut",
        "which-languages-can-i-add",
        "why-does-a-selectable-language-have-few-or-no-names",
        "name-not-available",
    }
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.motion_demos: list[dict[str, str]] = []
        self.motion_fallbacks: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append((attribute, values[attribute]))
        if tag == "img":
            classes = set(values.get("class", "").split())
            if "motion-demo" in classes:
                self.motion_demos.append(values)
            if "motion-fallback" in classes:
                self.motion_fallbacks.append(values)


def output_path_for_reference(site: Path, page: Path, reference: str) -> tuple[Path, str]:
    parsed = urlsplit(reference)
    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)
    if raw_path.startswith("/"):
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


def validate(site: Path) -> list[str]:
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
        for attribute, reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme.lower() in ignored_schemes or reference.startswith("//"):
                continue
            target, fragment = output_path_for_reference(site, page, reference)
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

        if len(parser.motion_demos) != len(parser.motion_fallbacks):
            errors.append(
                f"{route}: motion demos and fallbacks must be paired "
                f"({len(parser.motion_demos)} demos, {len(parser.motion_fallbacks)} fallbacks)"
            )
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
    arguments = argument_parser.parse_args()
    site = arguments.site.resolve()
    if not site.is_dir():
        argument_parser.error(f"generated site directory does not exist: {site}")

    errors = validate(site)
    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Website validation passed: {site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
