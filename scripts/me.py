"""Keep wiki/me.md, the user's preferences and needs, learned across sessions.

wiki/me.md sits in the wiki and is gitignored. CLAUDE.md loads it into every session; its
"Self-evolving" section says when to write to it. This script keeps the file's layout fixed:
two sections, `## Preferences` and `## Needs`, one bullet per fact, each ending `(yyyy-mm-dd)`.

Commands:
- init: create wiki/me.md with the empty layout, if it is missing.
- add <preference|need> <text>: append a dated bullet to that section. Creates wiki/me.md if
  missing. Skips the bullet when the same text is already there. --skill names the skill or
  reference file that now holds the rule, for a lesson also written into .claude-dev/.
- show: print the bullets, optionally of one section.

To change or delete a bullet, edit wiki/me.md directly.

Usage:
    uv run scripts/me.py init
    uv run scripts/me.py add preference "Experience bullets: labels only when a job spans areas"
    uv run scripts/me.py add preference "No overlapping labels" --skill resume
    uv run scripts/me.py add need "A one-page resume for each job ad"
    uv run scripts/me.py show --section preference
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import textwrap
from pathlib import Path

ME = Path(__file__).resolve().parent.parent / "wiki" / "me.md"
SECTIONS = {"preference": "## Preferences", "need": "## Needs"}
WIDTH = 96

LAYOUT = """\
# Me

What I prefer and need from this repo, learned while working with Claude. Private: gitignored.
Claude adds a bullet when I steer, correct or confirm something, and edits or deletes bullets
that change. Rules that hold for anyone using the pipeline go into `.claude-dev/` instead.

## Preferences

## Needs
"""


def init() -> bool:
    """Create wiki/me.md with the empty layout. Return True if it was created."""
    if ME.exists():
        return False
    ME.write_text(LAYOUT)
    return True


def bullets(text: str) -> dict[str, list[str]]:
    """Split wiki/me.md into its sections' bullets, each joined onto one line."""
    out: dict[str, list[str]] = {h: [] for h in SECTIONS.values()}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.strip() if line.strip() in out else None
        elif current and line.startswith("- "):
            out[current].append(line[2:].strip())
        elif current and line.startswith("  ") and out[current]:
            out[current][-1] += " " + line.strip()
    return out


def normalise(s: str) -> str:
    s = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$", "", s)
    return re.sub(r"\W+", " ", s).strip().lower()


def add(section: str, text: str, skill: str | None, date: str) -> str:
    init()
    heading = SECTIONS[section]
    content = ME.read_text()
    if heading not in content:
        content = content.rstrip("\n") + f"\n\n{heading}\n"
    text = text.strip().rstrip(".") + "."
    if skill:
        text += f" Now in the `{skill}` skill."
    if any(normalise(b).startswith(normalise(text)) for b in bullets(content)[heading]):
        return f"already in {heading}: {text}"

    bullet = textwrap.fill(f"{text} ({date})", width=WIDTH, initial_indent="- ", subsequent_indent="  ")
    lines = content.splitlines()
    start = lines.index(heading)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    block = ["", bullet] if end == start + 1 else [bullet]
    lines[end:end] = block
    ME.write_text("\n".join(lines).rstrip("\n") + "\n")
    return f"added to {heading}: {bullet}"


def show(section: str | None) -> None:
    if not ME.exists():
        print("wiki/me.md is missing; run: uv run scripts/me.py init")
        return
    for heading, items in bullets(ME.read_text()).items():
        if section and heading != SECTIONS[section]:
            continue
        print(heading)
        for item in items or ["(none)"]:
            print(f"- {item}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create wiki/me.md if it is missing")
    p_add = sub.add_parser("add", help="append a dated bullet")
    p_add.add_argument("section", choices=SECTIONS)
    p_add.add_argument("text")
    p_add.add_argument("--skill", help="skill or reference file that now holds the rule")
    p_add.add_argument("--date", default=dt.date.today().isoformat(), help="yyyy-mm-dd")
    p_show = sub.add_parser("show", help="print the bullets")
    p_show.add_argument("--section", choices=SECTIONS)
    args = parser.parse_args()

    if args.command == "init":
        print("created wiki/me.md" if init() else "wiki/me.md already exists")
    elif args.command == "add":
        print(add(args.section, args.text, args.skill, args.date))
    else:
        show(args.section)
    return 0


if __name__ == "__main__":
    sys.exit(main())
