"""Export my git commits from the cloned repos of one company to CSV.

Reads every repo under raw/<company>/repos/<id>/<slug>/, on all refs, and keeps the commits
whose author matches `me` in raw/<company>/mapping.yml (names as case-insensitive substrings,
emails case-insensitive exact). Columns:

    timestamp, hash, title, description, author

`timestamp` is the author date in ISO 8601, `title` the subject line, `description` the body
(may span lines; CSV quotes it), `author` is "Name <email>". Rows are oldest first. With
--with-source, `project` and `repo` (the slug) come first, since one hash may appear in more
than one clone.

Commit messages can hold client names, so the default output is raw/<company>/my-commits.csv,
which is gitignored. Pass `-o -` to print to stdout.

Usage:
    uv run scripts/my_commits.py <company>
    uv run scripts/my_commits.py <company> --project retail-shelf-cv --project hitl-chatbot
    uv run scripts/my_commits.py <company> --repo backend --with-source
    uv run scripts/my_commits.py <company> --since 2025-01-01 -o -
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["timestamp", "hash", "title", "description", "author"]
REC, UNIT = "\x1e", "\x1f"


def is_me(name: str, email: str, me: dict) -> bool:
    """Match an author against `me`."""
    if any(e.lower() == email.lower() for e in me.get("emails", [])):
        return True
    return any(n.lower() in name.lower() for n in me.get("names", []))


def my_commits(repo: Path, me: dict, since: str | None) -> list[dict]:
    """Return my commits in repo, on all refs."""
    fmt = REC + UNIT.join(["%aI", "%H", "%s", "%b", "%an", "%ae"])
    args = ["git", "-C", str(repo), "log", "--all", f"--format={fmt}"]
    if since:
        args.append(f"--since={since}")
    out = subprocess.run(args, capture_output=True, text=True, errors="replace", check=True).stdout
    rows = []
    for record in out.split(REC)[1:]:
        date, sha, subject, body, name, email = record.split(UNIT, 5)
        email = email.strip()
        if is_me(name, email, me):
            rows.append(
                {
                    "timestamp": date,
                    "hash": sha,
                    "title": subject.strip(),
                    "description": body.strip(),
                    "author": f"{name} <{email}>",
                }
            )
    return rows


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("company")
    parser.add_argument("--project", action="append", help="only this project id (repeatable)")
    parser.add_argument("--repo", action="append", help="only the repo with this slug (repeatable)")
    parser.add_argument("--since", help="only commits after this date, e.g. 2025-01-01")
    parser.add_argument("--with-source", action="store_true", help="add project and repo columns")
    parser.add_argument("-o", "--output", help="CSV path, or - for stdout")
    args = parser.parse_args()

    base = ROOT / "raw" / args.company
    mapping = base / "mapping.yml"
    if not mapping.exists():
        sys.exit(f"missing {mapping}")
    me = yaml.safe_load(mapping.read_text()).get("me") or {}
    if not me.get("names") and not me.get("emails"):
        sys.exit(f"no me.names or me.emails in {mapping}")

    repos = sorted(p.parent for p in (base / "repos").glob("*/*/.git"))
    if args.project:
        repos = [p for p in repos if p.parent.name in args.project]
    if args.repo:
        repos = [p for p in repos if p.name in args.repo]
    if not repos:
        sys.exit(f"no cloned repos match under {base / 'repos'}; run ingest_repos.py first")

    rows = []
    for repo in repos:
        for row in my_commits(repo, me, args.since):
            rows.append({"project": repo.parent.name, "repo": repo.name, **row})
    rows.sort(key=lambda r: r["timestamp"])

    fields = (["project", "repo"] if args.with_source else []) + FIELDS
    output = args.output or str(base / "my-commits.csv")
    if output == "-":
        try:
            write_csv(sys.stdout, fields, rows)
        except BrokenPipeError:  # reader closed early, e.g. `| head`
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    else:
        with open(output, "w", newline="", encoding="utf-8") as f:
            write_csv(f, fields, rows)
        print(f"{len(rows)} commits from {len(repos)} repos -> {output}", file=sys.stderr)
    return 0


def write_csv(f, fields: list[str], rows: list[dict]) -> None:
    """Write rows as CSV with a header."""
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
