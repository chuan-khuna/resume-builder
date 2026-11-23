"""Clone or fetch every git source in raw/<company>/mapping.yml and count my commits.

Each source lands in raw/<company>/<id>/<repo-name>/. A missing target is cloned; an existing
one is fetched with --all --prune. Failures are recorded and the run continues. After loading,
each repo's commits on all refs are matched against `me` (names as case-insensitive substrings,
emails case-insensitive exact). The results are written to raw/<company>/summary.json
(per project and per repo) and printed as a table.

Usage:
    uv run scripts/ingest_repos.py <company>
    uv run scripts/ingest_repos.py <company> --jobs 8
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class RepoResult:
    """Outcome of loading one source."""

    project: str
    repo: str
    url: str
    action: str  # cloned | fetched | failed
    error: str = ""
    my_commits: int = 0
    total_commits: int = 0
    first: str = ""
    last: str = ""


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


def load(project: str, url: str, base: Path, me: dict) -> RepoResult:
    """Clone or fetch one source, then count my commits."""
    name = repo_name(url)
    target = base / project / name
    result = RepoResult(project=project, repo=name, url=url, action="")
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
    me = mapping.get("me", {})
    tasks = [(p["id"], url) for p in mapping.get("projects", []) for url in p.get("sources", [])]

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda t: load(t[0], t[1], base, me), tasks))

    (base / "summary.json").write_text(json.dumps(summarize(mapping, results), indent=2, ensure_ascii=False) + "\n")

    current = None
    for r in results:
        if r.project != current:
            current = r.project
            print(f"\n## {current}")
            print(f"{'repo':45} {'status':8} {'mine':>5} {'total':>6}  range / error")
        flag = "  <-- ZERO" if r.action != "failed" and r.my_commits == 0 else ""
        detail = r.error if r.action == "failed" else f"{r.first} ~ {r.last}{flag}"
        print(f"{r.repo:45} {r.action:8} {r.my_commits:>5} {r.total_commits:>6}  {detail}")

    failed = sum(r.action == "failed" for r in results)
    print(f"\n{len(results)} sources, {failed} failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
