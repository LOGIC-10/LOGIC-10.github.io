#!/usr/bin/env python3
"""Offline audit of every local HTML href, src, srcset, and fragment."""

import argparse
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit


PROJECT = Path(__file__).resolve().parent.parent
LOCAL_ORIGIN = "https://offline.invalid"


def srcset_urls(value):
    """Read srcset URL tokens, preserving commas inside data URLs."""
    position = 0
    while position < len(value):
        while position < len(value) and (value[position].isspace() or value[position] == ","):
            position += 1
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        candidate = value[start:position]
        if not candidate:
            break
        if candidate.endswith(","):
            yield candidate.rstrip(",")
            continue
        yield candidate
        parentheses = 0
        while position < len(value):
            character = value[position]
            position += 1
            if character == "(":
                parentheses += 1
            elif character == ")" and parentheses:
                parentheses -= 1
            elif character == "," and not parentheses:
                break


@dataclass
class Reference:
    attribute: str
    value: str
    line: int


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = Counter()
        self.anchors = set()
        self.references = []
        self.base = None
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if attributes.get("id") is not None:
            self.ids[attributes["id"]] += 1
        if tag == "a" and attributes.get("name") is not None:
            self.anchors.add(attributes["name"])
        if tag == "base" and self.base is None and attributes.get("href") is not None:
            self.base = attributes["href"]
        for attribute in ("href", "src", "data-document-url"):
            if attributes.get(attribute) is not None:
                self.references.append(Reference(attribute, attributes[attribute], self.getpos()[0]))
        if attributes.get("srcset") is not None:
            self.references.extend(
                Reference("srcset", url, self.getpos()[0])
                for url in srcset_urls(attributes["srcset"])
            )

    handle_startendtag = handle_starttag


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=PROJECT / "dist", help="built site directory")
    args = parser.parse_args()
    root = args.dist.resolve()
    if not root.is_dir():
        print("Built site is missing: run `npm run build` before this audit.", file=sys.stderr)
        return 1
    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        print(f"No HTML pages found in {root}.", file=sys.stderr)
        return 1
    pages = {}
    errors = []
    for path in html_files:
        try:
            pages[path.resolve()] = Page(path)
        except (OSError, UnicodeError) as error:
            errors.append(f"{path.relative_to(root)}: cannot read HTML: {error}")
    local_count = external_count = fragment_count = 0
    for path, page in pages.items():
        label = path.relative_to(root).as_posix()
        for identifier, count in page.ids.items():
            if count > 1:
                errors.append(f"{label}: duplicate id {identifier!r} ({count} occurrences)")
        page_url = LOCAL_ORIGIN + "/" + label
        # A directory index is requested by its directory URL in the preview.
        if page_url.endswith("/index.html"):
            page_url = page_url[:-len("index.html")]
        try:
            base_url = urljoin(page_url, page.base) if page.base is not None else page_url
        except ValueError as error:
            errors.append(f"{label}: invalid base URL: {error}")
            base_url = page_url
        for reference in page.references:
            location = f"{label}:{reference.line} {reference.attribute}={reference.value!r}"
            try:
                url = urlsplit(urljoin(base_url, reference.value.strip()))
                if url.scheme not in ("http", "https") or url.netloc != "offline.invalid":
                    external_count += 1
                    continue
                local_count += 1
                decoded = unquote(url.path, errors="strict")
                if "\x00" in decoded or "\\" in decoded:
                    errors.append(f"{location}: invalid local path")
                    continue
                target = (root / decoded.lstrip("/")).resolve()
                if not target.is_relative_to(root):
                    errors.append(f"{location}: path escapes dist")
                    continue
                if target.is_dir():
                    target = target / "index.html"
                if not target.is_file():
                    errors.append(f"{location}: missing file {target.relative_to(root)}")
                    continue
                if not url.fragment or target.suffix.lower() != ".html":
                    continue
                fragment = unquote(url.fragment, errors="strict").split(":~:", 1)[0]
                if not fragment or fragment.lower() == "top":
                    continue
                fragment_count += 1
                destination = pages.get(target.resolve())
                if destination is None:
                    errors.append(f"{location}: target HTML could not be parsed")
                elif fragment not in destination.ids and fragment not in destination.anchors:
                    errors.append(f"{location}: missing anchor #{fragment} in {target.relative_to(root)}")
            except (UnicodeError, ValueError, OSError) as error:
                errors.append(f"{location}: invalid URL ({error})")
    if errors:
        print(f"FAIL: {len(errors)} issue(s) in {len(pages)} HTML page(s).")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        f"PASS: {len(pages)} HTML page(s), {local_count} local references, "
        f"{fragment_count} fragment references; {external_count} external/non-file references skipped."
    )
    print("Offline check only; external destinations were not requested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
