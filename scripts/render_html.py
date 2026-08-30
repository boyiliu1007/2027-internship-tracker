#!/usr/bin/env python3
"""Renders one of the listings/*.md pipe-table files as a standalone,
styled HTML page (no external dependencies). Used by local_refresh.sh
so the lists can be viewed in a browser without an IDE or markdown app.
"""
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def cell_to_html(cell: str) -> str:
    return LINK_RE.sub(r'<a href="\2" target="_blank" rel="noopener">\1</a>', cell.strip())


def render(md_path: Path) -> str:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("#").strip() if lines and lines[0].startswith("#") else md_path.stem

    table_lines = [l for l in lines if l.strip().startswith("|")]
    rows = [
        [c for c in l.strip().strip("|").split("|")]
        for l in table_lines
        if not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", l)
    ]

    head_row, *body_rows = rows if rows else ([], [])
    thead = "".join(f"<th>{cell_to_html(c)}</th>" for c in head_row)
    tbody = "".join(
        "<tr>" + "".join(f"<td>{cell_to_html(c)}</td>" for c in row) + "</tr>"
        for row in body_rows
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 2rem; background: #121212; color: #eaeaea; font-size: 1.15rem; }}
  h1 {{ font-size: 1.9rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 1.05rem; }}
  th, td {{ border: 1px solid #3a3a3a; padding: 10px 14px; text-align: left; vertical-align: top; }}
  th {{ background: #1e1e1e; position: sticky; top: 0; }}
  tr:nth-child(even) {{ background: #1a1a1a; }}
  a {{ color: #6ab0ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head><body>
<h1>{title}</h1>
<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>
</body></html>
"""


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(render(src), encoding="utf-8")
