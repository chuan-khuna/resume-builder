"""Render a brag document to HTML: evidence/<company>/brag-document.md -> brag-document.html.

The HTML is a view of the Markdown, which is itself a view of the evidence: never edit the HTML.
It follows the page contract in docs/shared/doc.js, so it gets the shared themes and table of
contents. The front matter becomes the byline; `user:` block markers stay as HTML comments.
Links to evidence files keep pointing at the .md files beside the page.

Usage:
    uv run scripts/brag_html.py themather
    uv run scripts/brag_html.py evidence/themather/brag-document.md
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "docs" / "shared"
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render(md_path: Path) -> str:
    text = md_path.read_text()
    meta: dict = {}
    if m := FRONT_MATTER.match(text):
        meta = yaml.safe_load(m.group(1)) or {}
        text = text[m.end() :]
    # "My part:" follows its project line with no blank line; keep it on a line of its own.
    text = text.replace("\nMy part:", "\\\n<em>My part:</em>")

    md =MarkdownIt("commonmark", {"html": True}).enable("table")
    tokens = md.parse(text)
    title = "Brag document"
    seen: set[str] = set()
    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        content = tokens[i + 1].content
        if tok.tag == "h1":
            title = content
            continue
        slug, n = slugify(content), 2
        while slug in seen:
            slug, n = f"{slugify(content)}-{n}", n + 1
        seen.add(slug)
        tok.attrSet("id", slug)

    # The h1 goes in the page header; drop it from the body.
    body_tokens, skip = [], 0
    for tok in tokens:
        if tok.type == "heading_open" and tok.tag == "h1":
            skip = 3
        if skip:
            skip -= 1
            continue
        body_tokens.append(tok)
    body = md.renderer.render(body_tokens, md.options, {})

    rel = Path("../" * len(md_path.resolve().parent.relative_to(ROOT).parts))
    css, js = rel / "docs/shared/globals.css", rel / "docs/shared/doc.js"
    byline = " · ".join(
        html.escape(str(v))
        for v in (meta.get("period"), meta.get("role"), meta.get("built_from"), meta.get("updated"))
        if v
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css}">
  <script src="{js}"></script>
</head>
<body data-doc-name="Brag document">
<!-- Generated from {md_path.name} by scripts/brag_html.py. Do not edit: rebuild instead. -->
<main class="doc">

<header class="doc-head">
  <h1>{html.escape(title)}</h1>
  <p class="byline">{byline}</p>
</header>

{body}
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", help="a company slug, or the path to a brag-document.md")
    args = parser.parse_args()
    path = Path(args.target)
    if not path.suffix:
        path = ROOT / "evidence" / args.target / "brag-document.md"
    if not path.is_file():
        print(f"not found: {path}", file=sys.stderr)
        return 1
    if not SHARED.is_dir():
        print(f"missing shared doc assets: {SHARED}", file=sys.stderr)
        return 1
    out = path.with_suffix(".html")
    out.write_text(render(path))
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
