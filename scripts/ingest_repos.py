"""Clone or fetch every git source in raw/<company>/mapping.yml and count my commits.

Each source is `{url, slug}`; `slug` is the repo's anonymised name. The source lands in
raw/<company>/repos/<id>/<slug>/. A missing target is cloned; an existing one is fetched with
--all --prune. Failures are recorded and the run continues. After loading, each repo's commits
on all refs are matched against `me` (names as case-insensitive substrings, emails
case-insensitive exact). The results are written to raw/<company>/commit-summary.json (per
project and per repo) and printed as a table.

A fetch moves only the remote branches, so after it the checked-out branch is fast-forwarded to
its upstream (skipped when the working tree has changes or the branch has diverged). Blame and
the `verified:` sha read the checked-out branch, so each repo also lists `branches_ahead`: the
remote branches that hold my commits the checked-out branch does not have.

The mapping is checked before anything is loaded: every source needs a `url` and a `slug`,
and a slug is lowercase kebab-case and unique within its project.

Usage:
    uv run scripts/ingest_repos.py <company>
    uv run scripts/ingest_repos.py <company> --jobs 8
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class RepoResult:
    """Outcome of loading one source."""

    project: str
    slug: str
    repo: str  # real repo name from the URL; stays in raw/
    url: str
    action: str  # cloned | fetched | failed
    error: str = ""
    my_commits: int = 0
    total_commits: int = 0
    first: str = ""
    last: str = ""
    head_branch: str = ""
    update: str = ""  # fast-forwarded N | up to date | skipped: <reason>
    branches_ahead: dict[str, int] = field(default_factory=dict)  # branch -> my commits not in HEAD


def repo_name(url: str) -> str:
    """Return the URL's last path segment without `.git`."""
    last = url.rstrip("/").split("/")[-1].split(":")[-1]
    return last.removesuffix(".git")


def run_git(args: list[str], timeout: int = 900) -> subprocess.CompletedProcess[str]:
    """Run git non-interactively."""
    env = {"GIT_TERMINAL_PROMPT": "0", "GIT_SSH_COMMAND": "ssh -o BatchMode=yes"}

    return subprocess.run(["git", *args], capture_output=True, text=True, timeout=timeout, env={**os.environ, **env})


def is_me(name: str, email: str, me: dict) -> bool:
    """Match a commit author against `me`."""
    name_l, email_l = name.lower(), email.lower()
    if any(e.lower() == email_l for e in me.get("emails", [])):
        return True
    return any(n.lower() in name_l for n in me.get("names", []))


def check_sources(mapping: dict) -> list[str]:
    """Return one error per malformed source in mapping.yml."""
    errors = []
    for p in mapping.get("projects", []):
        pid = p.get("id", "?")
        seen: set[str] = set()
        for i, src in enumerate(p.get("sources") or []):
            where = f"projects[{pid}].sources[{i}]"
            if not isinstance(src, dict):
                errors.append(f"{where}: write it as {{url: ..., slug: ...}}, not a bare URL")
                continue
            if not src.get("url"):
                errors.append(f"{where}: url is missing")
            slug = str(src.get("slug") or "")
            if not SLUG.match(slug):
                errors.append(f"{where}: slug {slug!r} must be lowercase kebab-case, like 'backend'")
            elif slug in seen:
                errors.append(f"{where}: slug {slug!r} is used twice in this project")
            seen.add(slug)
    return errors


def fast_forward(target: Path) -> str:
    """Fast-forward the checked-out branch to its upstream; return what happened."""
    if run_git(["-C", str(target), "status", "--porcelain"]).stdout.strip():
        return "skipped: working tree has changes"
    behind = run_git(["-C", str(target), "rev-list", "--count", "HEAD..@{u}"])
    if behind.returncode != 0:
        return "skipped: no upstream"
    if behind.stdout.strip() == "0":
        return "up to date"
    proc = run_git(["-C", str(target), "merge", "--ff-only", "@{u}"])
    return f"fast-forwarded {behind.stdout.strip()}" if proc.returncode == 0 else "skipped: diverged from upstream"


def branches_ahead(target: Path, me: dict) -> dict[str, int]:
    """Return remote branches with my commits that HEAD lacks, and how many."""
    refs = run_git(["-C", str(target), "for-each-ref", "refs/remotes", "--format=%(refname:short)"])
    ahead = {}
    for ref in refs.stdout.split():
        if ref.endswith("/HEAD") or "/" not in ref:
            continue
        log = run_git(["-C", str(target), "log", f"HEAD..{ref}", "--format=%an%x09%ae"])
        mine = sum(is_me(*line.split("\t", 1), me) for line in log.stdout.splitlines() if "\t" in line)
        if mine:
            ahead[ref] = mine
    return dict(sorted(ahead.items(), key=lambda kv: -kv[1]))


def load(project: str, src: dict, base: Path, me: dict) -> RepoResult:
    """Clone or fetch one source, then count my commits."""
    url, slug = src["url"], src["slug"]
    target = base / "repos" / project / slug
    result = RepoResult(project=project, slug=slug, repo=repo_name(url), url=url, action="")
    try:
        if (target / ".git").exists():
            proc = run_git(["-C", str(target), "fetch", "--all", "--prune"])
            result.action = "fetched"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            proc = run_git(["clone", url, str(target)])
            result.action = "cloned"
    except subprocess.TimeoutExpired:
        result.action, result.error = "failed", "timeout"
        return result
    if proc.returncode != 0:
        result.action = "failed"
        result.error = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else f"exit {proc.returncode}"
        return result

    result.update = fast_forward(target) if result.action == "fetched" else "up to date"
    result.head_branch = run_git(["-C", str(target), "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    result.branches_ahead = branches_ahead(target, me)

    log = run_git(["-C", str(target), "log", "--all", "--format=%an%x09%ae%x09%aI"])
    dates = []
    for line in log.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        result.total_commits += 1
        if is_me(parts[0], parts[1], me):
            result.my_commits += 1
            dates.append(parts[2][:10])
    if dates:
        result.first, result.last = min(dates), max(dates)
    return result


def summarize(mapping: dict, results: list[RepoResult]) -> dict:
    """Group repo results by project, with totals and my commit date range."""
    projects = []
    for p in mapping.get("projects", []):
        repos = [r for r in results if r.project == p["id"]]
        firsts = [r.first for r in repos if r.first]
        lasts = [r.last for r in repos if r.last]
        projects.append(
            {
                "id": p["id"],
                "title": p.get("title", ""),
                "my_commits": sum(r.my_commits for r in repos),
                "total_commits": sum(r.total_commits for r in repos),
                "first": min(firsts, default=""),
                "last": max(lasts, default=""),
                "repos": [
                    {k: v for k, v in asdict(r).items() if k != "project"}
                    | {"zero_commits": r.action != "failed" and r.my_commits == 0}
                    for r in repos
                ],
            }
        )
    return {
        "company": mapping.get("company", ""),
        "generated": datetime.now(UTC).isoformat(timespec="seconds"),
        "sources": len(results),
        "failed": sum(r.action == "failed" for r in results),
        "projects": projects,
    }


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("company")
    parser.add_argument("--jobs", type=int, default=6)
    args = parser.parse_args()

    base = ROOT / "raw" / args.company
    mapping = yaml.safe_load((base / "mapping.yml").read_text())
    errors = check_sources(mapping)
    if errors:
        print("mapping.yml has malformed sources:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1
    me = mapping.get("me", {})
    tasks = [(p["id"], src) for p in mapping.get("projects", []) for src in p.get("sources") or []]

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda t: load(t[0], t[1], base, me), tasks))

    (base / "commit-summary.json").write_text(
        json.dumps(summarize(mapping, results), indent=2, ensure_ascii=False) + "\n"
    )

    current = None
    for r in results:
        if r.project != current:
            current = r.project
            print(f"\n## {current}")
            print(f"{'slug':20} {'repo':45} {'status':8} {'mine':>5} {'total':>6}  range / error")
        flag = "  <-- ZERO" if r.action != "failed" and r.my_commits == 0 else ""
        detail = r.error if r.action == "failed" else f"{r.first} ~ {r.last}{flag}"
        print(f"{r.slug:20} {r.repo:45} {r.action:8} {r.my_commits:>5} {r.total_commits:>6}  {detail}")
        if r.update.startswith(("fast-forwarded", "skipped")):
            print(f"{'':20} {r.head_branch}: {r.update}")
        for ref, n in r.branches_ahead.items():
            print(f"{'':20} {ref}: {n} commits of mine not in {r.head_branch}")

    failed = sum(r.action == "failed" for r in results)
    print(f"\n{len(results)} sources, {failed} failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
