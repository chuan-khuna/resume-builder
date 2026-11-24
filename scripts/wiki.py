"""Keep the LLM wiki in wiki/: append log entries and check the wiki's structure.

The rules are in wiki/CLAUDE.md. This script does the bookkeeping that needs no judgement.

Commands:
- log <op> <title>: append `## [yyyy-mm-dd HH:MM] <op> | <title>` to wiki/logs/<today>.md,
  with one bullet per --line. Creates the day's file if missing.
- lint: check the notes. Errors (exit 1): broken [[links]], notes missing from index.md,
  index entries with no note, bad frontmatter, `sources:` paths that do not exist.
  Warnings: orphan notes (no inbound link but the index's), raw files no note cites.
- pending: list raw files no note cites yet, oldest first: what is left to ingest.

Usage:
    uv run scripts/wiki.py log ingest "RAG survey" --line "Source: raw/2026-11-24-rag-survey.pdf"
    uv run scripts/wiki.py lint
    uv run scripts/wiki.py lint --json
    uv run scripts/wiki.py pending
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

WIKI = Path(__file__).resolve().parent.parent / "wiki"
NOTES, RAW, LOGS = WIKI / "notes", WIKI / "raw", WIKI / "logs"
OPS = ("ingest", "query", "lint", "schema")
TYPES = ("source", "entity", "concept", "topic", "answer")
REQUIRED = ("title", "type", "sources", "created", "updated")
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def log(op: str, title: str, lines: list[str], now: dt.datetime) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)
    path = LOGS / f"{now:%Y-%m-%d}.md"
    text = path.read_text() if path.exists() else f"# {now:%Y-%m-%d}\n"
    entry = f"## [{now:%Y-%m-%d %H:%M}] {op} | {title}\n" + "".join(f"- {ln}\n" for ln in lines)
    path.write_text(text.rstrip("\n") + "\n\n" + entry)
    return path


def read_notes() -> dict[str, tuple[dict | None, str]]:
    """Map each note's slug to (frontmatter or None, body)."""
    notes = {}
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text()
        m = FRONTMATTER.match(text)
        try:
            meta = yaml.safe_load(m.group(1)) if m else None
        except yaml.YAMLError:
            meta = None
        notes[path.stem] = (meta if isinstance(meta, dict) else None, text[m.end() :] if m else text)
    return notes


def raw_files() -> list[str]:
    return sorted(
        str(p.relative_to(WIKI))
        for p in RAW.rglob("*")
        if p.is_file() and p.name != "README.md" and not p.name.startswith(".")
    )


def cited(notes: dict) -> set[str]:
    return {s for meta, _ in notes.values() if meta for s in meta.get("sources") or []}


def lint() -> dict[str, list[str]]:
    notes = read_notes()
    errors: list[str] = []
    warnings: list[str] = []
    inbound: dict[str, set[str]] = {slug: set() for slug in notes}

    for slug, (meta, body) in notes.items():
        for target in {t.strip() for t in LINK.findall(body)}:
            if target not in notes:
                errors.append(f"{slug}: broken link [[{target}]]")
            elif target != slug:
                inbound[target].add(slug)
        if slug == "index":
            continue
        if meta is None:
            errors.append(f"{slug}: missing or invalid frontmatter")
            continue
        missing = [k for k in REQUIRED if k not in meta]
        if missing:
            errors.append(f"{slug}: frontmatter lacks {', '.join(missing)}")
        if meta.get("type") not in TYPES:
            errors.append(f"{slug}: type {meta.get('type')!r} is not one of {', '.join(TYPES)}")
        for src in meta.get("sources") or []:
            if not (WIKI / src).exists():
                errors.append(f"{slug}: source {src} does not exist")

    indexed = [t.strip() for t in LINK.findall(notes["index"][1])] if "index" in notes else []
    if "index" not in notes:
        errors.append("index: notes/index.md is missing")
    for slug in notes:
        if slug != "index" and slug not in indexed:
            errors.append(f"index: [[{slug}]] is not listed")
        if slug != "index" and not inbound[slug] - {"index"}:
            warnings.append(f"{slug}: orphan, no note links to it but the index")
    for slug in {s for s in indexed if indexed.count(s) > 1}:
        errors.append(f"index: [[{slug}]] is listed more than once")

    done = cited(notes)
    warnings += [f"{f}: not ingested, no note cites it" for f in raw_files() if f not in done]
    return {"errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_log = sub.add_parser("log", help="append a log entry")
    p_log.add_argument("op", choices=OPS)
    p_log.add_argument("title")
    p_log.add_argument("--line", action="append", default=[], help="a bullet under the entry")
    p_lint = sub.add_parser("lint", help="check the notes")
    p_lint.add_argument("--json", action="store_true")
    sub.add_parser("pending", help="raw files not yet ingested")
    args = parser.parse_args()

    if args.command == "log":
        print(log(args.op, args.title, args.line, dt.datetime.now()).relative_to(WIKI.parent))
        return 0
    if args.command == "pending":
        done = cited(read_notes())
        for f in raw_files():
            if f not in done:
                print(f)
        return 0

    result = lint()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for kind in ("errors", "warnings"):
            print(f"{kind}: {len(result[kind])}")
            for item in result[kind]:
                print(f"  {item}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
