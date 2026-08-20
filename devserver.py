#!/usr/bin/env python3
"""Static dev server that refuses to cache.

Python's stock http.server sends no Cache-Control, so browsers fall back to
heuristic caching and will happily serve a stale HTML page (and the stale CSS
it references) with no revalidation. That looks exactly like a broken layout
and wastes a lot of time. This sends no-store on everything.
"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8199
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    ThreadingHTTPServer(("127.0.0.1", port),
                        lambda *a, **k: NoCacheHandler(*a, directory=root, **k)).serve_forever()
