#!/usr/bin/env python3
"""Audit built inline papers, talks, report images, and file-link boundaries."""

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
import logging
from pathlib import Path
import re
import sys
from urllib.parse import parse_qsl, unquote, urljoin, urlsplit

try:
    from pypdf import PdfReader
except ImportError:
    print("FAIL: this audit requires pypdf in the Python environment.", file=sys.stderr)
    sys.exit(1)


PROJECT = Path(__file__).resolve().parent.parent
ORIGIN = "https://inline-audit.invalid"
EXPECTED_PAGES = {
    "repoagent": 29,
    "proactive-agent": 27,
    "escapebench": 23,
    "long-context-bias": 13,
    "ui-tars-2": 30,
    "seed-1-8": 51,
    "seed-2-0": 87,
    "seed-2-1": 73,
    "agent-world": 48,
    "world-model-tool": 38,
    "on-policy-distillation-ii": 29,
    "boundary-certificate-proofs": 9,
    "test-time-exploration": 12,
    "repoagent-slides": 35,
    "repoagent-poster": 1,
}
TALK_IDS = {"repoagent-slides", "repoagent-poster"}
PAPER_IDS = set(EXPECTED_PAGES) - TALK_IDS
EXPECTED_HTML = {
    "index.html", "about/index.html", "research/index.html",
    "projects/index.html", "projects/stethoscope/index.html",
    "notes/index.html", "notes/deepseek-r1/index.html",
    *(f"research/{slug}/index.html" for slug in PAPER_IDS | {"xagent"}),
}
XAGENT_IMAGES = {
    "overview.png", "workflow.png", "demo.gif", "statistics.png",
    "ask_for_human_help.png", "bert_1.png", "bert_2.png", "bert_3.png",
    "agent_comparison.png", "eval_on_dataset.png",
}
XAGENT_HEADINGS = (
    "Introduction", "XAgent", "ToolServer", "Quickstart",
    "Build and Setup ToolServer", "Setup and Run XAgent", "Demo",
    "Case 1. Data Analysis: Demonstrating the Effectiveness of Dual-Loop Mechanism",
    "Case 2. Recommendation: A New Paradigm of Human-Agent Interaction",
    "Case 3. Training Model: A Sophisticated Tool User",
    "Evaluation", "Blog", "Our Contributors", "Citation",
)
FILE_EXTENSION = re.compile(
    r"\.(?:pdf|pptx?|docx?|xlsx?|zip|rar|7z|tar(?:\.gz)?|tgz|od[ptfs]|"
    r"rtf|csv|tsv|epub|mp4|webm|mov|mp3|wav|ogg)$", re.I
)
IMAGE_EXTENSION = re.compile(r"\.(?:png|jpe?g|gif|webp|avif|svg|tiff?|bmp|ico)$", re.I)
CV_NAME = re.compile(r"(?:^|[-_.\s])(?:cv|resume|curriculum[-_\s]*vitae)(?:$|[-_.\s])", re.I)
EMAIL = "qinyuluo123@gmail.com"


def normalized(value):
    return " ".join(value.split())


@dataclass
class Element:
    tag: str
    attributes: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    line: int = 0

    def descendants(self, tag=None):
        for child in self.children:
            if isinstance(child, Element):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.descendants(tag)

    def text(self):
        if self.tag in {"script", "style"}:
            return ""
        return " ".join(child.text() if isinstance(child, Element) else child for child in self.children)


class Page(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        node = Element(tag, dict(attributes), line=self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for position in range(len(self.stack) - 1, 0, -1):
            if self.stack[position].tag == tag:
                del self.stack[position:]
                break

    def handle_data(self, value):
        self.stack[-1].children.append(value)

    def by_id(self, identifier):
        return [node for node in self.root.descendants() if node.attributes.get("id") == identifier]


def local_file(root, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
        raise ValueError("expected a local absolute URL")
    decoded = unquote(parsed.path, errors="strict")
    if "\\" in decoded or "\x00" in decoded:
        raise ValueError("invalid local path")
    target = (root / decoded.lstrip("/")).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("path escapes asset directory")
    return target


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.digest()


def direct_file_url(url):
    """Recognize explicit file URLs, including extensionless scholarly PDFs."""
    parsed = urlsplit(url)
    path = unquote(parsed.path).rstrip("/")
    if FILE_EXTENSION.search(path):
        return True
    host = (parsed.hostname or "").lower()
    if (host == "arxiv.org" or host.endswith(".arxiv.org")) and re.match(r"^/pdf(?:/|$)", path, re.I):
        return True
    if (host == "openreview.net" or host.endswith(".openreview.net")) and path.lower() == "/pdf":
        return True
    if path.lower().endswith(("/download_pub", "/download_supplementary")):
        return True
    for key, value in parse_qsl(parsed.query):
        if key.lower() in {"filename", "file", "download", "attachment"} and FILE_EXTENSION.search(unquote(value)):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=PROJECT / "dist")
    args = parser.parse_args()
    dist = args.dist.resolve()
    public = PROJECT / "public"
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)
        return condition

    manifest_path = PROJECT / "src/data/document-assets.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"FAIL: cannot read document manifest: {error}")
        return 1
    if not isinstance(manifest, dict):
        print("FAIL: document manifest must be an object keyed by document id.")
        return 1
    require(set(manifest) == set(EXPECTED_PAGES), "Manifest must contain all 13 papers/reports, the 35-slide deck, and one-page poster.")
    require(dist.is_dir(), "Built site is missing; run npm run build before this audit.")

    total_pages = 0
    valid_pdfs = 0
    # Some original conference PDFs contain duplicate dictionary keys. Their
    # warnings do not change the page-count checks or the delivered source bytes.
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    for identifier, expected in EXPECTED_PAGES.items():
        row = manifest.get(identifier)
        if not require(isinstance(row, dict), f"{identifier}: missing document record."):
            continue
        require(row.get("id") == identifier, f"{identifier}: mismatched manifest id.")
        require(row.get("format") == "pdf", f"{identifier}: expected PDF format.")
        require(row.get("pageCount") == expected, f"{identifier}: expected {expected} declared pages.")
        require(row.get("src") == f"/documents/{identifier}.pdf", f"{identifier}: unexpected document URL.")
        require(bool(row.get("title")) and str(row.get("source", "")).startswith("https://"), f"{identifier}: missing title or public source.")
        try:
            source = local_file(public, row.get("src", ""))
            delivered = local_file(dist, row.get("src", ""))
            if not require(source.is_file() and source.stat().st_size > 0, f"{identifier}: public PDF is missing or empty."):
                continue
            with source.open("rb") as stream:
                require(stream.read(5) == b"%PDF-", f"{identifier}: asset is not a PDF.")
            reader = PdfReader(source)
            actual = len(reader.pages)
            total_pages += actual
            require(actual == expected == row.get("pageCount"), f"{identifier}: actual PDF has {actual} pages; expected {expected}.")
            for number, page in enumerate(reader.pages, 1):
                require(float(page.mediabox.width) > 0 and float(page.mediabox.height) > 0, f"{identifier}: page {number} has invalid dimensions.")
            if row.get("fileBytes") is not None:
                require(source.stat().st_size == row["fileBytes"], f"{identifier}: byte count differs from manifest.")
            if require(delivered.is_file() and delivered.stat().st_size > 0, f"{identifier}: built PDF is missing or empty; rebuild the site."):
                require(digest(source) == digest(delivered), f"{identifier}: built PDF differs from public asset; rebuild the site.")
            valid_pdfs += 1
        except Exception as error:
            errors.append(f"{identifier}: cannot read PDF ({error}).")
    expected_total = sum(EXPECTED_PAGES.values())
    require(valid_pdfs == len(EXPECTED_PAGES) and total_pages == expected_total, f"Expected {len(EXPECTED_PAGES)} readable PDFs / {expected_total} pages; found {valid_pdfs} PDFs / {total_pages} pages.")
    math_record = manifest.get("boundary-certificate-proofs", {})
    require(math_record.get("title") == "The Sharp Numerical-Range Spectral-Set Inequality" and "Earlier manuscript version" in math_record.get("versionNote", ""), "Mathematics PDF must identify the earlier manuscript version and its actual title.")

    pages = {}
    for path in sorted(dist.rglob("*.html")):
        label = path.relative_to(dist).as_posix()
        try:
            pages[label] = Page(path)
        except (OSError, UnicodeError) as error:
            errors.append(f"{label}: cannot parse HTML ({error}).")
    require(set(pages) == EXPECTED_HTML, f"Expected {len(EXPECTED_HTML)} site pages; missing={sorted(EXPECTED_HTML - set(pages))}, extra={sorted(set(pages) - EXPECTED_HTML)}.")

    def check_reader(label, identifier, section_id):
        page = pages.get(label)
        if page is None:
            return
        sections = page.by_id(section_id)
        if not require(len(sections) == 1, f"{label}: expected one #{section_id} inline reader."):
            return
        section = sections[0]
        row = manifest.get(identifier, {})
        require(section.tag == "section" and "data-document-reader" in section.attributes, f"{label}: #{section_id} is not a document reader.")
        require(section.attributes.get("data-document-url") == row.get("src"), f"{label}: inline PDF URL differs from manifest.")
        require(section.attributes.get("data-document-pages") == str(EXPECTED_PAGES[identifier]), f"{label}: reader has wrong page count.")
        controls = {key for node in section.descendants() for key in node.attributes}
        for attribute in ("data-document-prev", "data-document-next", "data-document-page", "data-document-search", "data-document-find", "data-document-zoom", "data-document-expand", "data-document-container", "data-document-viewer"):
            require(attribute in controls, f"{label}: reader is missing {attribute}.")
        if row.get("versionNote"):
            require(normalized(row["versionNote"]) in normalized(section.text()), f"{label}: manuscript version note is absent from the reader.")

    for identifier in sorted(PAPER_IDS):
        check_reader(f"research/{identifier}/index.html", identifier, "full-text")
    for identifier in sorted(TALK_IDS):
        check_reader("notes/index.html", identifier, identifier)
    all_reader_urls = Counter(node.attributes["data-document-url"] for page in pages.values() for node in page.root.descendants() if "data-document-url" in node.attributes)
    expected_urls = Counter(f"/documents/{identifier}.pdf" for identifier in EXPECTED_PAGES)
    require(all_reader_urls == expected_urls, f"Built HTML must contain exactly one reader for each of the {len(EXPECTED_PAGES)} PDFs.")

    xagent = pages.get("research/xagent/index.html")
    if xagent is not None:
        sections = xagent.by_id("full-text")
        if require(len(sections) == 1, "XAgent: expected one #full-text report."):
            report = sections[0]
            headings = [normalized(node.text()) for node in report.descendants() if re.fullmatch(r"h[2-6]", node.tag)]
            for heading in XAGENT_HEADINGS:
                require(any(value == heading or value.endswith(" " + heading) for value in headings), f"XAgent: missing report section {heading!r}.")
            require(len(normalized(report.text())) >= 8000, "XAgent: full report text is unexpectedly short.")
            images = list(report.descendants("img"))
            expected_images = {f"/images/xagent-report/{name}" for name in XAGENT_IMAGES}
            require(len(images) == 10 and {node.attributes.get("src") for node in images} == expected_images, "XAgent: expected all ten local report images, without remote replacements.")
            for image_url in sorted(expected_images):
                for root in (public, dist):
                    image = local_file(root, image_url)
                    require(image.is_file() and image.stat().st_size > 0, f"XAgent: image {image_url} missing or empty in {root.name}.")

    anchor_count = 0
    for label, page in pages.items():
        page_url = ORIGIN + "/" + label.removesuffix("index.html")
        for anchor in page.root.descendants("a"):
            anchor_count += 1
            attributes = anchor.attributes
            location = f"{label}:{anchor.line}"
            require("download" not in attributes, f"{location}: anchor has a download attribute.")
            href = attributes.get("href")
            if href is None:
                continue
            try:
                url = urljoin(page_url, href.strip())
                parsed = urlsplit(url)
                require(not direct_file_url(url), f"{location}: direct file anchor {href!r}; link to the inline content or publication record.")
                if parsed.netloc == "inline-audit.invalid":
                    require(not IMAGE_EXTENSION.search(unquote(parsed.path)), f"{location}: local raw-image anchor {href!r}; use the in-page image viewer.")
                label_text = normalized(anchor.text()).lower()
                require(not (CV_NAME.search(unquote(parsed.path)) or label_text in {"cv", "resume", "curriculum vitae", "download cv", "view cv", "read cv"}), f"{location}: CV publication link is present.")
            except ValueError as error:
                errors.append(f"{location}: invalid anchor URL {href!r} ({error}).")
        require(any(anchor.attributes.get("href") == f"mailto:{EMAIL}" for anchor in page.root.descendants("a")), f"{label}: contact email link is missing.")
    for label in ("index.html", "about/index.html"):
        if label in pages:
            require("ByteDance Seed" in normalized(pages[label].root.text()), f"{label}: ByteDance Seed affiliation is missing.")
            require(EMAIL in normalized(pages[label].root.text()), f"{label}: visible contact email is missing.")
    for root in (public, dist):
        for path in root.rglob("*"):
            if path.is_file():
                require(not (CV_NAME.search(path.name) or path.stem.lower().endswith("cv")), f"CV file is published in {root.name}: {path.relative_to(root)}.")

    if errors:
        print(f"FAIL: {len(errors)} inline-content issue(s).")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: {valid_pdfs} PDFs / {total_pages} pages; {len(PAPER_IDS)} paper/report readers, full XAgent report / 10 local images, 35 slides and one-page poster.")
    print(f"PASS: {len(pages)} HTML pages / {anchor_count} anchors; no download attributes, direct document-file links, local raw-image links, or published CV; email and affiliation retained.")
    print("Offline artifact audit only; browser rendering, reader interactions, and external destinations require separate checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
