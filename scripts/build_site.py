#!/usr/bin/env python3
"""Builds the static site/ directory published to GitHub Pages: dark,
readable HTML renders of the listings tables (no Jekyll, no deps)."""
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_html import render  # noqa: E402

PAGES = [
    ("software-engineering.md", "software-engineering.html", "Software Engineering"),
    ("data-science-ai-machine-learning.md", "data-science-ai-machine-learning.html", "Data Science, AI & Machine Learning"),
]


def build():
    SITE_DIR.mkdir(exist_ok=True)
    refreshed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    links = []
    for src_name, dst_name, label in PAGES:
        src = ROOT / "listings" / src_name
        html = render(src)
        (SITE_DIR / dst_name).write_text(html, encoding="utf-8")
        links.append((dst_name, label))

    link_items = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in links)
    index_html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>2027 Internship Tracker</title>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 2rem; background: #121212; color: #eaeaea; font-size: 1.15rem; }}
  h1 {{ font-size: 1.9rem; }}
  ul {{ font-size: 1.2rem; line-height: 2.2rem; }}
  a {{ color: #6ab0ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .meta {{ color: #999; font-size: 0.95rem; }}
</style>
</head><body>
<h1>2027 Internship Tracker</h1>
<p class="meta">Last refreshed: {refreshed_at}</p>
<ul>{link_items}</ul>
</body></html>
"""
    (SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Site built in {SITE_DIR} ({len(links)} pages).")


if __name__ == "__main__":
    build()
