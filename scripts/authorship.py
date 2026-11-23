"""Report my authorship in each repo of one project in raw/<company>/repos/<id>/.

Repos are named by their `slug` from mapping.yml, the anonymised name evidence cites.

Per repo, on all refs:
- authors (`git shortlog -sne --all`);
- per directory, two levels deep: my commit count and my share of `git blame` lines at HEAD;
- my commits: sha, date, message, files touched (skip with --no-commits);
- branches ahead: remote branches holding my commits that the read ref lacks.

Blame and the head sha read HEAD, the checked-out branch, unless --ref <slug>=<ref> names
another ref. When "branches ahead" lists a branch with real work of mine, rerun with --ref on
it (or its merge into a later branch) so blame and `verified:` cover that work.

`me` (names as case-insensitive substrings, emails case-insensitive exact) comes from
raw/<company>/mapping.yml. In update mode pass --since-sha <repo>=<sha> to list only my commits
after that sha; <repo> is the slug.

Usage:
    uv run scripts/authorship.py <company> <id>
    uv run scripts/authorship.py <company> <id> --repo backend --no-commits
    uv run scripts/authorship.py <company> <id> --since-sha backend=a1b2c3d
    uv run scripts/authorship.py <company> <id> --ref backend=origin/dev
    uv run scripts/authorship.py <company> <id> --json
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP_BLAME_SUFFIXES = (".lock", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".pt", ".onnx", ".mp4", ".zip")


def git(repo: Path, *args: str) -> str:
    """Run git in repo and return stdout."""
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, errors="replace")
    return proc.stdout


def is_me(name: str, email: str, me: dict) -> bool:
    """Match an author against `me`."""
    if any(e.lower() == email.lower() for e in me.get("emails", [])):
        return True
    return any(n.lower() in name.lower() for n in me.get("names", []))


def area(path: str, depth: int = 2) -> str:
    """Return the directory of path, cut to depth levels; root files map to '.'."""
    parts = path.split("/")[:-1][:depth]
    return "/".join(parts) if parts else "."


def head_sha(repo: Path, ref: str = "HEAD") -> str:
    """Return the sha of ref."""
    return git(repo, "rev-parse", ref).strip()


def branches_ahead(repo: Path, me: dict, ref: str) -> dict[str, int]:
    """Return remote branches with my commits that ref lacks, and how many."""
    ahead = {}
    for branch in git(repo, "for-each-ref", "refs/remotes", "--format=%(refname:short)").split():
        if branch.endswith("/HEAD") or "/" not in branch:
            continue
        log = git(repo, "log", f"{ref}..{branch}", "--format=%an%x09%ae")
        mine = sum(is_me(*line.split("\t", 1), me) for line in log.splitlines() if "\t" in line)
        if mine:
            ahead[branch] = mine
    return dict(sorted(ahead.items(), key=lambda kv: -kv[1]))


def commits(repo: Path, me: dict, since: str | None) -> tuple[list[dict], dict[str, int]]:
    """Return my commits (newest first) and my commit count per area."""
    rng = ["--all", f"^{since}"] if since else ["--all"]
    out = git(repo, "log", *rng, "--name-only", "--format=\x1e%H\t%an\t%ae\t%aI\t%s")
    mine, per_area = [], defaultdict(int)
    for block in out.split("\x1e")[1:]:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        sha, name, email, date, subject = lines[0].split("\t", 4)
        if not is_me(name, email, me):
            continue
        files = lines[1:]
        mine.append({"sha": sha[:9], "date": date[:10], "message": subject, "files": files})
        for a in {area(f) for f in files}:
            per_area[a] += 1
    return mine, dict(per_area)


def blame_shares(repo: Path, me: dict, ref: str = "HEAD") -> dict[str, tuple[int, int]]:
    """Return {area: (my lines, total lines)} from git blame at ref."""
    shares: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for path in git(repo, "ls-tree", "-r", "--name-only", ref).splitlines():
        if path.endswith(SKIP_BLAME_SUFFIXES) or "lock" in Path(path).name:
            continue
        out = git(repo, "blame", "--line-porcelain", ref, "--", path)
        name = email = ""
        a = area(path)
        for line in out.splitlines():
            if line.startswith("author "):
                name = line[7:]
            elif line.startswith("author-mail "):
                email = line[12:].strip("<>")
            elif line.startswith("\t"):
                shares[a][1] += 1
                if is_me(name, email, me):
                    shares[a][0] += 1
    return {k: (v[0], v[1]) for k, v in shares.items()}


def report(repo: Path, me: dict, since: str | None, with_commits: bool, ref: str = "HEAD") -> dict:
    """Build the authorship report for one repo, with blame read at ref."""
    mine, per_area = commits(repo, me, since)
    shares = blame_shares(repo, me, ref)
    areas = sorted(set(shares) | set(per_area))
    return {
        "repo": repo.name,
        "ref": git(repo, "rev-parse", "--abbrev-ref", ref).strip() or ref,
        "head": head_sha(repo, ref),
        "branches_ahead": branches_ahead(repo, me, ref),
        "authors": git(repo, "shortlog", "-sne", "--all").strip().splitlines(),
        "areas": [
            {
                "area": a,
                "my_commits": per_area.get(a, 0),
                "my_lines": shares.get(a, (0, 0))[0],
                "lines": shares.get(a, (0, 0))[1],
                "share": round(100 * shares[a][0] / shares[a][1]) if shares.get(a, (0, 0))[1] else None,
            }
            for a in areas
        ],
        "my_commits": mine if with_commits else len(mine),
    }


def print_report(r: dict) -> None:
    """Print one repo report as text."""
    print(f"\n# {r['repo']}  {r['ref']} {r['head'][:9]}")
    for branch, n in r["branches_ahead"].items():
        print(f"  ! {branch}: {n} commits of mine not in {r['ref']}; blame does not see them")
    print("## authors")
    for a in r["authors"]:
        print(f"  {a}")
    print(f"## areas\n  {'area':50} {'commits':>7} {'lines':>12} {'share':>6}")
    for a in r["areas"]:
        share = f"{a['share']}%" if a["share"] is not None else "-"
        print(f"  {a['area']:50} {a['my_commits']:>7} {a['my_lines']:>5}/{a['lines']:<6} {share:>6}")
    if isinstance(r["my_commits"], list):
        print(f"## my commits ({len(r['my_commits'])})")
        for c in r["my_commits"]:
            print(f"  {c['sha']} {c['date']} {c['message']}  [{len(c['files'])} files]")
    else:
        print(f"## my commits: {r['my_commits']}")


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("company")
    parser.add_argument("id")
    parser.add_argument("--repo", help="only the repo with this slug")
    parser.add_argument("--since-sha", action="append", default=[], help="<repo>=<sha>, update mode")
    parser.add_argument("--ref", action="append", default=[], help="<repo>=<ref>: blame at this ref, not HEAD")
    parser.add_argument("--no-commits", action="store_true", help="omit my commit list")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    base = ROOT / "raw" / args.company
    me = yaml.safe_load((base / "mapping.yml").read_text()).get("me", {})
    since = dict(s.split("=", 1) for s in args.since_sha)
    refs = dict(s.split("=", 1) for s in args.ref)
    repos = sorted(p for p in (base / "repos" / args.id).iterdir() if (p / ".git").exists())
    if args.repo:
        repos = [p for p in repos if p.name == args.repo]
    reports = [report(p, me, since.get(p.name), not args.no_commits, refs.get(p.name, "HEAD")) for p in repos]
    if args.json:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    else:
        for r in reports:
            print_report(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
