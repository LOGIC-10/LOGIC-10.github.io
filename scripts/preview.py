#!/usr/bin/env python3
"""Serve only the built site, on the local loopback interface."""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


DIST = Path(__file__).resolve().parent.parent / "dist"


class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def safe_path(self):
        try:
            path = unquote(urlsplit(self.path).path, errors="strict")
            parts = path.split("/")
            if "\x00" in path or "\\" in path or any(
                part.startswith(".") for part in parts if part
            ):
                return None
            target = (DIST / path.lstrip("/")).resolve()
            if not target.is_relative_to(DIST.resolve()):
                return None
            return target
        except (UnicodeError, ValueError, OSError):
            return None

    def translate_path(self, path):
        # send_head validates this before the standard handler uses it.
        return str(self.safe_path())

    def send_head(self):
        if self.safe_path() is None:
            self.send_error(404, "Not found")
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "Not found")
        return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4174, help="local port (default: 4174)")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    if not DIST.is_dir() or not (DIST / "index.html").is_file():
        print("Built site is missing: run `npm run build` before `npm run preview`.", file=sys.stderr)
        return 1
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), PreviewHandler)
    except OSError as error:
        print(f"Cannot start local preview on port {args.port}: {error}", file=sys.stderr)
        return 1
    print(f"Preview: http://127.0.0.1:{args.port}/ (serving dist only)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
