"""Print one project's Jira tickets from raw/<company>/jira/merged.json.

A project's tickets are chosen by its `jira` selectors in raw/<company>/mapping.yml:

    projects:
      - id: retail-shelf-cv
        jira:
          - project: SHELF            # every ticket in this Jira project (older projects)
          - project: TT               # only the tickets under this epic, in a shared
            epic: Retail shelf        # project such as a tech-team board

`project` matches the Jira project key or name; `epic` matches the epic title. Both are
case-insensitive. With --text, tickets whose title or detail contains the text are added too.

Usage:
    uv run scripts/jira_tickets.py <company> <id>
    uv run scripts/jira_tickets.py <company> <id> --text shelf --text planogram
    uv run scripts/jira_tickets.py <company> <id> --json
    uv run scripts/jira_tickets.py <company> --unmapped    # tickets no project selects
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def selected(ticket: dict, selectors: list[dict]) -> bool:
    """True when any selector picks this ticket."""
    project = ticket.get("project") or {}
    names = {(project.get("key") or "").lower(), (project.get("name") or "").lower()}
    epic = ((ticket.get("epic") or {}).get("title") or "").lower()
    for sel in selectors:
        if str(sel.get("project", "")).lower() not in names:
            continue
        if "epic" in sel and str(sel["epic"]).lower() != epic:
            continue
        return True
    return False


def line(t: dict) -> str:
    epic = (t.get("epic") or {}).get("title") or "-"
    return f"{t['created']}  {t['key']:<12} {t['type'] or '':<8} {t['status'] or '':<12} [{epic}] {t['title']}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("company")
    parser.add_argument("id", nargs="?", help="project id in mapping.yml")
    parser.add_argument("--text", action="append", default=[], help="also match this text in title or detail")
    parser.add_argument("--json", action="store_true", help="print the tickets as JSON")
    parser.add_argument("--unmapped", action="store_true", help="list tickets that no project's selectors pick")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    base = ROOT / "raw" / args.company
    mapping = yaml.safe_load((base / "mapping.yml").read_text(encoding="utf-8"))
    tickets = json.loads((base / "jira" / "merged.json").read_text(encoding="utf-8"))

    if args.unmapped:
        selectors = [s for p in mapping["projects"] for s in p.get("jira") or []]
        rest = [t for t in tickets if not selected(t, selectors)]
        groups = Counter((t["project"]["key"], (t.get("epic") or {}).get("title")) for t in rest if t.get("project"))
        print(f"{len(rest)} of {len(tickets)} tickets are not selected by any project:")
        for (key, epic), n in groups.most_common():
            print(f"  {n:4}  {key}" + (f" / {epic}" if epic else ""))
        return

    if not args.id:
        parser.error("give a project id, or --unmapped")
    project = next((p for p in mapping["projects"] if p["id"] == args.id), None)
    if project is None:
        raise SystemExit(f"no project {args.id!r} in mapping.yml")
    selectors = project.get("jira") or []
    texts = [x.lower() for x in args.text]
    hits = [
        t
        for t in tickets
        if selected(t, selectors) or any(x in f"{t['title']} {t.get('detail') or ''}".lower() for x in texts)
    ]
    if not selectors and not texts:
        print(f"{args.id} has no jira selectors in mapping.yml; pass --text to search", file=sys.stderr)
    if args.json:
        print(json.dumps(hits, indent=2, ensure_ascii=False))
        return
    for t in hits:
        print(line(t))
    if hits:
        print(f"\n{len(hits)} tickets, {hits[0]['created']} ~ {hits[-1]['created']}")


if __name__ == "__main__":
    main()
