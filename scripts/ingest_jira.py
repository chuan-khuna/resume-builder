"""Download the Jira tickets assigned to me into raw/<company>/jira/, trimmed to the key fields.

Writes one file per year created, raw/<company>/jira/<yyyy>.json, then merges every year into
raw/<company>/jira/merged.json. Each ticket keeps only:

    key, title, detail, type, status, project, epic, parent, assignee, created, resolved

`detail` is the description as plain text. `project` is `{key, name}`. `epic` is `{key, title}`
of the parent when the parent is an epic; `parent` is the direct parent key (a story, for a
sub-task). Dates are yyyy-mm-dd.

Two sources, same output:

- REST API (default): basic auth with `jira.email` and `jira.api_token` from
  raw/<company>/mapping.yml, searching `assignee = currentUser() ORDER BY created ASC`.
- --from-raw FILE...: Jira search results saved as JSON, for example from the Atlassian MCP
  tool `searchJiraIssuesUsingJql`. Each file holds a search response (`{"issues": [...]}`) or
  a list of issues, optionally wrapped in `{"data": ...}` as the MCP returns it. Each issue
  needs `key` and `fields` as the Jira REST API returns them.

Each run replaces the yearly files and merged.json.

Usage:
    uv run scripts/ingest_jira.py <company>
    uv run scripts/ingest_jira.py <company> --jql 'assignee = currentUser() AND project = ABC'
    uv run scripts/ingest_jira.py <company> --from-raw /tmp/jira-page-1.json /tmp/jira-page-2.json
    uv run scripts/ingest_jira.py <company> --merge-only
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JQL = "assignee = currentUser() ORDER BY created ASC"
FIELDS = ["summary", "description", "issuetype", "status", "project", "parent", "assignee", "created", "resolutiondate"]
PAGE_SIZE = 100


# ---------- Trimming ----------


def adf_text(node: object) -> str:
    """Flatten an Atlassian Document Format node (or a plain string) to text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_text(n) for n in node)
    if not isinstance(node, dict):
        return ""
    kind = node.get("type")
    if kind == "text":
        return node.get("text", "")
    if kind == "hardBreak":
        return "\n"
    if kind in ("mention", "emoji"):
        return node.get("attrs", {}).get("text", "")
    if kind == "inlineCard":
        return node.get("attrs", {}).get("url", "")
    inner = adf_text(node.get("content", []))
    if kind == "listItem":
        return "- " + inner.strip() + "\n"
    if kind in ("paragraph", "heading", "codeBlock", "blockquote", "rule", "table", "tableRow"):
        return inner.rstrip() + "\n"
    return inner


def name_of(obj: dict | None, key: str = "name") -> str | None:
    return obj.get(key) if obj else None


def plain(text: str) -> str:
    """Strip HTML tags and entities from a description the MCP returned as HTML."""
    if "<" not in text:
        return text
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", text)
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def is_subtask(issuetype: dict | None) -> bool:
    if not issuetype:
        return False
    if "subtask" in issuetype:
        return bool(issuetype["subtask"])
    return (issuetype.get("name") or "").lower().replace("-", "") == "subtask"


def trim(issue: dict) -> dict:
    """Keep the fields evidence needs from one Jira issue."""
    f = issue.get("fields", {})
    parent = f.get("parent")
    parent_type = name_of((parent or {}).get("fields", {}).get("issuetype"))
    epic = None
    # The parent's type is missing from some MCP views. In Jira's hierarchy the parent of a
    # ticket that is not a sub-task is an epic, so infer it.
    if (
        parent
        and (parent_type or "").lower() == "epic"
        or parent
        and not parent_type
        and not is_subtask(f.get("issuetype"))
    ):
        epic = {"key": parent.get("key"), "title": parent.get("fields", {}).get("summary")}
    description = f.get("description")
    detail = (plain(description) if isinstance(description, str) else adf_text(description)).strip()
    project = f.get("project")
    return {
        "key": issue.get("key"),
        "title": f.get("summary"),
        "detail": detail or None,
        "type": name_of(f.get("issuetype")),
        "status": name_of(f.get("status")),
        "project": {"key": project.get("key"), "name": project.get("name")} if project else None,
        "epic": epic,
        "parent": parent.get("key") if parent else None,
        "assignee": name_of(f.get("assignee"), "displayName"),
        "created": (f.get("created") or "")[:10] or None,
        "resolved": (f.get("resolutiondate") or "")[:10] or None,
    }


# ---------- Sources ----------


def fetch_api(jira: dict, jql: str) -> tuple[list[dict], int | None]:
    """Page through /rest/api/3/search/jql. Return the issues and the approximate total."""
    for field in ("site", "email", "api_token"):
        value = str(jira.get(field) or "")
        if not value or value.startswith("<"):
            raise SystemExit(f"mapping.yml: jira.{field} is not set. Fill it in, or use --from-raw.")
    base = f"https://{jira['site']}"
    token = base64.b64encode(f"{jira['email']}:{jira['api_token']}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Accept": "application/json", "Content-Type": "application/json"}

    def call(method: str, path: str, params: dict | None = None, body: dict | None = None) -> dict:
        url = base + path + ("?" + urllib.parse.urlencode(params) if params else "")
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            raise SystemExit(f"Jira {method} {path}: HTTP {err.code}: {err.read().decode()[:300]}") from err

    try:
        total = call("POST", "/rest/api/3/search/approximate-count", body={"jql": jql.split(" ORDER BY")[0]}).get(
            "count"
        )
    except SystemExit:
        total = None

    issues: list[dict] = []
    token_next: str | None = None
    while True:
        params = {"jql": jql, "fields": ",".join(FIELDS), "maxResults": PAGE_SIZE}
        if token_next:
            params["nextPageToken"] = token_next
        page = call("GET", "/rest/api/3/search/jql", params=params)
        issues += page.get("issues", [])
        token_next = page.get("nextPageToken")
        if page.get("isLast", True) or not token_next:
            break
    return issues, total


def read_raw(paths: list[Path]) -> list[dict]:
    """Read issues from saved search results."""
    issues: list[dict] = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("data", data).get("issues", [])  # the MCP wraps responses in "data"
        issues += [i for i in data if isinstance(i, dict) and i.get("key")]
    return issues


# ---------- Output ----------


def write_years(out: Path, tickets: list[dict]) -> dict[str, int]:
    """Replace jira/<yyyy>.json with the tickets grouped by year created."""
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("[0-9][0-9][0-9][0-9].json"):
        old.unlink()
    years: dict[str, list[dict]] = {}
    for t in tickets:
        years.setdefault((t["created"] or "unknown")[:4], []).append(t)
    for year, items in years.items():
        items.sort(key=lambda t: (t["created"] or "", t["key"]))
        (out / f"{year}.json").write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {y: len(v) for y, v in sorted(years.items())}


def merge(out: Path) -> list[dict]:
    """Merge every jira/<yyyy>.json into jira/merged.json, oldest first, one entry per key."""
    by_key: dict[str, dict] = {}
    for path in sorted(out.glob("[0-9][0-9][0-9][0-9].json")):
        for t in json.loads(path.read_text(encoding="utf-8")):
            by_key[t["key"]] = t
    merged = sorted(by_key.values(), key=lambda t: (t["created"] or "", t["key"]))
    (out / "merged.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return merged


def report(merged: list[dict], total: int | None) -> None:
    print(f"tickets: {len(merged)}" + (f" (search reported about {total})" if total is not None else ""))
    print(
        "per year:   "
        + ", ".join(f"{y} {n}" for y, n in sorted(Counter(t["created"][:4] for t in merged if t["created"]).items()))
    )
    print(
        "per project: "
        + ", ".join(
            f"{p} {n}" for p, n in Counter(t["project"]["key"] if t["project"] else None for t in merged).most_common()
        )
    )
    epics = Counter(t["epic"]["key"] for t in merged if t["epic"])
    print(f"with an epic: {sum(epics.values())} tickets under {len(epics)} epics")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("company")
    parser.add_argument("--jql", default=DEFAULT_JQL, help=f"search (default: {DEFAULT_JQL!r})")
    parser.add_argument(
        "--from-raw", nargs="+", type=Path, metavar="FILE", help="saved search results instead of the API"
    )
    parser.add_argument("--merge-only", action="store_true", help="rebuild merged.json from the yearly files")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    company_dir = ROOT / "raw" / args.company
    out = company_dir / "jira"
    total = None
    if not args.merge_only:
        if args.from_raw:
            issues = read_raw(args.from_raw)
        else:
            mapping = yaml.safe_load((company_dir / "mapping.yml").read_text(encoding="utf-8"))
            if not mapping.get("jira"):
                raise SystemExit("mapping.yml has no jira block: nothing to download.")
            issues, total = fetch_api(mapping["jira"], args.jql)
        tickets: dict[str, dict] = {}
        for t in map(trim, issues):
            tickets.setdefault(t["key"], t)  # a key seen twice keeps its first copy
        tickets = list(tickets.values())
        written = write_years(out, tickets)
        print("wrote " + ", ".join(f"jira/{y}.json ({n})" for y, n in written.items()))
    merged = merge(out)
    print(f"wrote jira/merged.json ({len(merged)})")
    report(merged, total)


if __name__ == "__main__":
    main()
