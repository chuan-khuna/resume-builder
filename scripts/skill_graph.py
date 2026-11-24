"""Draw one company's skill graph: evidence/<company>/*.md -> evidence/<company>/skill-graph.html.

Nodes are areas, projects (one per evidence file), tools and keywords; colour shows the area.
Tools come from each evidence file's `tools:` line, keywords from its Summary and What I Did
sections, both matched against the shared taxonomy in .claude-dev/reference/skill-taxonomy.yml.
Each project's label, areas and hover description come from evidence/<company>/skill-graph.yml.

The graph is built and laid out with networkx (area hubs fixed on a ring, each node pulled to its
area) and drawn with pyvis (vis-network, inlined, so the page works offline). A panel on the page
runs the force simulation live, with sliders for its settings. Like the brag document it is a view of the evidence: never edit the HTML, rebuild it.

Usage:
    uv run scripts/skill_graph.py themather
"""

from __future__ import annotations

import argparse
import html
import json
import math
import random
import re
import sys
from pathlib import Path

import networkx as nx
import yaml
from pyvis.network import Network

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / ".claude-dev" / "reference" / "skill-taxonomy.yml"
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SECTION = re.compile(r"^## (.+)$", re.M)
# Items that say the work was not the user's, or did not ship, mark no keyword.
CAVEAT = re.compile(r"do not claim|reverted|switched off|removed from|is unknown|scope caveat|outside this repo", re.I)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def sections(body: str) -> dict[str, str]:
    """Split an evidence body into its `## ` sections, keyed by heading."""
    parts = SECTION.split(body)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def keyword_prose(body: str) -> str:
    """Summary (without its Remarks) and What I Did, minus the items that carry a caveat."""
    secs = sections(body)
    summary = re.split(r"^### Remarks\b", secs.get("Summary", ""), flags=re.M)[0]
    items = re.split(r"\n(?=\s*(?:- |\d+\. ))", summary + "\n" + secs.get("What I Did", ""))
    return "\n".join(i for i in items if not CAVEAT.search(i))


def tools_line(body: str) -> str:
    """The `tools:` line, up to "Studied, not used:" or the first blank line."""
    m = re.search(r"^tools:(.*?)(?:^Studied, not used:|\n\s*\n)", body, re.S | re.M)
    return m.group(1) if m else ""


def compile_matchers(entries: dict) -> list[tuple[str, str, re.Pattern]]:
    return [
        (name, spec["area"], re.compile(spec.get("match") or re.escape(name), re.I)) for name, spec in entries.items()
    ]


def short_period(period: str) -> str:
    """'2026-03 ~ 2026-11   # comment' -> '2026-03~2026-11'."""
    months = re.findall(r"\d{4}-\d{2}", str(period))
    return f"{months[0]}~{months[-1]}" if months else str(period)


def build(company: str) -> nx.Graph:
    folder = ROOT / "evidence" / company
    taxonomy = load_yaml(TAXONOMY)
    areas = taxonomy["areas"]
    settings = load_yaml(folder / "skill-graph.yml").get("projects", {})
    tools = compile_matchers(taxonomy["tools"])
    keywords = compile_matchers(taxonomy["keywords"])

    g = nx.Graph()
    for key, area in areas.items():
        g.add_node(f"a:{key}", kind="area", area=key, label=area["label"])

    for path in sorted(folder.glob("[0-9]*.md")):
        text = path.read_text(encoding="utf-8")
        m = FRONT_MATTER.match(text)
        if not m:
            continue
        meta, body = yaml.safe_load(m.group(1)), text[m.end() :]
        pid = meta["id"]
        conf = settings.get(pid)
        if not conf:
            sys.exit(f"{pid}: add it to evidence/{company}/skill-graph.yml")
        project_areas = conf["areas"]
        for a in project_areas:
            if a not in areas:
                sys.exit(f"{pid}: unknown area {a!r}")
        node = f"p:{pid}"
        g.add_node(
            node,
            kind="project",
            area=project_areas[0],
            areas=project_areas,
            label=conf["label"],
            period=short_period(meta.get("period", "")),
            description=" ".join(conf["description"].split()),
            status=meta.get("status", ""),
            file=path.name,
        )
        for i, a in enumerate(project_areas):
            g.add_edge(node, f"a:{a}", kind="area", main=i == 0)

        line = tools_line(body)
        prose = keyword_prose(body)
        for kind, matchers, text_ in (("tool", tools, line), ("keyword", keywords, prose)):
            for name, area, rx in matchers:
                if rx.search(text_):
                    nid = f"{kind[0]}:{name}"
                    g.add_node(nid, kind=kind, area=area, label=name)
                    g.add_edge(nid, node, kind=kind)
    return g


SCALE = 1000  # pixels per layout unit; the area hubs sit on a ring of radius 1
PULL_LENGTH = 90  # vis-network length of the hidden tool/keyword -> area edges


def layout(g: nx.Graph, areas: dict) -> dict[str, tuple[float, float]]:
    """Positions from networkx, in two passes, with the area hubs fixed on a ring.

    1. Projects alone, tied to their areas (the main area strongly), so each sits near its
       main hub instead of in a central pile of shared tools.
    2. Tools and keywords, with hubs and projects fixed, pulled by their projects and their
       own area hub; the pull grows with degree, or a tool many projects share (Docker,
       PostgreSQL) drifts to the centre.

    Done here rather than in the browser, so the page opens at once and already grouped.
    """
    hubs = {}
    for i, key in enumerate(areas):
        angle = -math.pi / 2 + 2 * math.pi * i / len(areas)
        hubs[f"a:{key}"] = (math.cos(angle), math.sin(angle))
    rng = random.Random(7)

    def near(hub: str, f: float, jitter: float) -> tuple[float, float]:
        hx, hy = hubs[hub]
        return (hx * f + rng.uniform(-jitter, jitter), hy * f + rng.uniform(-jitter, jitter))

    p1 = nx.Graph()
    p1.add_nodes_from(hubs)
    for u, v, d in g.edges(data=True):
        if d["kind"] == "area":
            p1.add_edge(u, v, weight=1.0 if d["main"] else 0.12)
    start = dict(hubs)
    for n, d in g.nodes(data=True):
        if d["kind"] == "project":
            start[n] = near(f"a:{d['area']}", 0.62, 0.1)
    pos = nx.spring_layout(p1, pos=start, fixed=list(hubs), k=0.2, iterations=300, weight="weight", seed=7)

    p2 = nx.Graph()
    p2.add_nodes_from(g)
    for u, v, d in g.edges(data=True):
        if d["kind"] != "area":
            p2.add_edge(u, v, weight=1.0)
    for n, d in g.nodes(data=True):
        if d["kind"] in ("tool", "keyword"):
            p2.add_edge(n, f"a:{d['area']}", weight=1.5 + 0.6 * g.degree(n))
            pos[n] = near(f"a:{d['area']}", 0.8, 0.15)
    fixed = [n for n, d in g.nodes(data=True) if d["kind"] in ("area", "project")]
    pos = nx.spring_layout(p2, pos=pos, fixed=fixed, k=0.09, iterations=400, weight="weight", seed=7)
    return {n: (float(x) * SCALE, float(y) * SCALE) for n, (x, y) in pos.items()}


def render(g: nx.Graph, company: str) -> str:
    areas = load_yaml(TAXONOMY)["areas"]
    pos = layout(g, areas)
    net = Network(height="100vh", width="100%", bgcolor="#ffffff", cdn_resources="in_line")
    projects = lambda n: [p for p in g[n] if g.nodes[p]["kind"] == "project"]  # noqa: E731
    font = {"face": "system-ui", "color": "#1f2937", "strokeWidth": 4, "strokeColor": "#ffffff"}

    for n, d in g.nodes(data=True):
        deg = g.degree(n)
        x, y = pos[n]
        common = dict(label=d["label"], color=areas[d["area"]]["color"], area=d["area"], kind=d["kind"], x=x, y=y)
        if d["kind"] == "area":
            net.add_node(
                n,
                shape="dot",
                size=38,
                title=f"{d['label']}: {len(projects(n))} projects",
                font={**font, "size": 40, "bold": True},
                borderWidth=6,
                fixed={"x": True, "y": True},
                **common,
            )
        elif d["kind"] == "project":
            net.add_node(
                n,
                shape="square",
                size=14 + deg**0.5 * 1.5,
                title=f"{d['period']}: {d['description']}",
                font={**font, "size": 24},
                file=d["file"],
                **common,
            )
        else:
            used = sorted(g.nodes[p]["label"] for p in projects(n))
            title = f"{d['label']} ({d['kind']}, {areas[d['area']]['label']})\nUsed in {len(used)}: " + ", ".join(used)
            net.add_node(
                n,
                shape="dot" if d["kind"] == "tool" else "diamond",
                size=5 + deg**0.5 * 2.5,
                title=title,
                font={**font, "size": 17},
                **common,
            )

    for u, v, d in g.edges(data=True):
        if d["kind"] == "area":
            net.add_edge(
                u,
                v,
                kind="area",
                color={"color": areas[g.nodes[v]["area"]]["color"], "opacity": 0.6 if d["main"] else 0.3},
                dashes=True,
                width=2 if d["main"] else 1,
            )
        else:
            net.add_edge(u, v, kind="link", color={"color": "#9ca3af", "opacity": 0.3}, width=1)
    # Hidden edges still pull when the simulation runs: they keep each tool and keyword near its hub.
    for n, d in g.nodes(data=True):
        if d["kind"] in ("tool", "keyword"):
            net.add_edge(n, f"a:{d['area']}", kind="pull", hidden=True, length=PULL_LENGTH)

    net.set_options(json.dumps(PHYSICS))
    page = net.generate_html()
    # pyvis links Bootstrap from a CDN for a card the page does not need: drop it so it works offline.
    page = re.sub(r"<link[^>]*bootstrap[^>]*>|<script[^>]*bootstrap[^>]*>\s*</script>", "", page)
    return page.replace("</body>", overlay(g, company, areas) + "\n</body>", 1)


# The layout comes from networkx, so the simulation starts off; the panel turns it on.
PHYSICS = {
    "physics": {
        "enabled": False,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
            "gravitationalConstant": -60,
            "centralGravity": 0.005,
            "springLength": 80,
            "springConstant": 0.06,
            "damping": 0.5,
            "avoidOverlap": 0.5,
        },
        "barnesHut": {
            "gravitationalConstant": -2400,
            "centralGravity": 0.1,
            "springLength": 80,
            "springConstant": 0.06,
            "damping": 0.5,
            "avoidOverlap": 0.5,
        },
        "stabilization": {"enabled": False},
    },
    "layout": {"improvedLayout": False},
    "interaction": {"hover": True, "tooltipDelay": 120, "hideEdgesOnDrag": True},
    "edges": {"smooth": False},
}


def overlay(g: nx.Graph, company: str, areas: dict) -> str:
    """Title, area legend, force panel and tooltip styling, added to pyvis's page."""
    counts = {k: sum(1 for _, d in g.nodes(data=True) if d["area"] == k and d["kind"] != "area") for k in areas}
    kinds = {k: sum(1 for _, d in g.nodes(data=True) if d["kind"] == k) for k in ("project", "tool", "keyword")}
    rows = "".join(
        f'<button data-area="{k}"><span style="background:{a["color"]}"></span>'
        f'{html.escape(a["label"])}<em>{counts[k]}</em></button>'
        for k, a in areas.items()
    )
    fa = PHYSICS["physics"]["forceAtlas2Based"]
    sliders = [
        # id, label, min, max, step, value
        ("repulsion", "Repulsion", 5, 300, 1, -fa["gravitationalConstant"]),
        ("central", "Central gravity", 0, 0.1, 0.001, fa["centralGravity"]),
        ("springLength", "Link length", 10, 300, 1, fa["springLength"]),
        ("springConstant", "Link strength", 0.005, 0.3, 0.005, fa["springConstant"]),
        ("pull", "Area pull length (shorter groups tighter)", 10, 400, 5, PULL_LENGTH),
        ("damping", "Damping", 0.05, 1, 0.01, fa["damping"]),
        ("overlap", "Avoid overlap", 0, 1, 0.05, fa["avoidOverlap"]),
    ]
    slider_html = "".join(
        f'<label>{lbl} <output id="o-{i}">{v}</output>'
        f'<input type="range" id="f-{i}" min="{lo}" max="{hi}" step="{st}" value="{v}"></label>'
        for i, lbl, lo, hi, st, v in sliders
    )
    return f"""
<style>
  body {{ margin: 0; font-family: system-ui, sans-serif; overflow: hidden; }}
  body > center {{ display: none; }}
  .card {{ border: 0 !important; }}
  div.vis-tooltip {{ white-space: normal !important; max-width: 340px; font: 13px/1.45 system-ui;
    padding: 8px 10px; border-radius: 6px; background: #fff; border: 1px solid #d1d5db;
    box-shadow: 0 4px 14px rgb(0 0 0 / .12); }}
  .sg-panel {{ position: fixed; top: 12px; z-index: 10; background: rgb(255 255 255 / .95);
    border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 14px; width: 260px;
    font-size: 13px; color: #1f2937; box-shadow: 0 4px 14px rgb(0 0 0 / .06);
    max-height: calc(100vh - 24px); overflow-y: auto; }}
  #sg-legend {{ left: 12px; }}
  #sg-forces {{ right: 12px; }}
  .sg-panel h1 {{ font-size: 15px; margin: 0 0 2px; }}
  .sg-panel h2 {{ font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: #6b7280;
    margin: 10px 0 4px; }}
  .sg-panel p {{ margin: 0 0 8px; color: #6b7280; font-size: 12px; }}
  #sg-legend button {{ display: flex; align-items: center; gap: 8px; width: 100%; background: none;
    border: 0; padding: 3px 4px; border-radius: 5px; font: inherit; color: inherit; cursor: pointer; }}
  #sg-legend button:hover {{ background: #f3f4f6; }}
  #sg-legend button.off {{ opacity: .35; }}
  #sg-legend button span {{ width: 11px; height: 11px; border-radius: 50%; flex: none; }}
  #sg-legend button em {{ margin-left: auto; font-style: normal; color: #9ca3af; }}
  #sg-forces label {{ display: block; margin: 0 0 6px; font-size: 12px; }}
  #sg-forces label output {{ float: right; color: #6b7280; font-variant-numeric: tabular-nums; }}
  #sg-forces input[type=range] {{ width: 100%; display: block; margin-top: 2px; }}
  #sg-forces .check {{ display: flex; align-items: center; gap: 6px; }}
  #sg-forces select {{ width: 100%; font: inherit; padding: 3px; }}
  #sg-forces .btns {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
  #sg-forces .btns button {{ border: 1px solid #d1d5db; background: #fff; border-radius: 6px;
    padding: 4px 9px; font: inherit; font-size: 12px; cursor: pointer; }}
  #sg-forces .btns button:hover {{ background: #f3f4f6; }}
  #sg-forces summary {{ font-weight: 600; cursor: pointer; }}
</style>
<div id="sg-legend" class="sg-panel">
  <h1>Skill graph: {html.escape(company)}</h1>
  <p>{kinds["project"]} projects (squares), {kinds["tool"]} tools (dots), {kinds["keyword"]} keywords
  (diamonds). Hover for details; double-click a project to open its evidence file.
  Click an area to hide it; double-click to show only it.</p>
  {rows}
</div>
<div id="sg-forces" class="sg-panel">
<details open>
  <summary>Forces and display</summary>
  <h2>Simulation</h2>
  <label class="check"><input type="checkbox" id="f-run"> Run the simulation</label>
  <label class="check"><input type="checkbox" id="f-pin" checked> Pin area hubs to the ring</label>
  <label>Solver <select id="f-solver">
    <option value="forceAtlas2Based">Force Atlas 2</option>
    <option value="barnesHut">Barnes-Hut</option>
  </select></label>
  <p>Moving a slider starts the simulation.</p>
  {slider_html}
  <h2>Show</h2>
  <label class="check"><input type="checkbox" id="s-labels" checked> Tool and keyword labels</label>
  <label class="check"><input type="checkbox" id="s-links" checked> Project-tool links</label>
  <label class="check"><input type="checkbox" id="s-area" checked> Project-area links</label>
  <div class="btns">
    <button id="b-stab">Stabilise</button>
    <button id="b-reset">Reset layout</button>
    <button id="b-fit">Fit</button>
    <button id="b-copy">Copy settings</button>
  </div>
</details>
</div>
<script>
(function () {{
  // ----- area legend -----
  const off = new Set();
  const all = {json.dumps(list(areas))};
  function applyAreas() {{
    nodes.update(nodes.get().map(n => ({{ id: n.id, hidden: off.has(n.area) }})));
    document.querySelectorAll('#sg-legend button').forEach(b =>
      b.classList.toggle('off', off.has(b.dataset.area)));
  }}
  document.querySelectorAll('#sg-legend button').forEach(b => {{
    let t;
    b.addEventListener('click', () => {{
      clearTimeout(t);
      t = setTimeout(() => {{
        const k = b.dataset.area;
        off.has(k) ? off.delete(k) : off.add(k);
        applyAreas();
      }}, 220);
    }});
    b.addEventListener('dblclick', () => {{
      clearTimeout(t);
      const k = b.dataset.area;
      const only = off.size === all.length - 1 && !off.has(k);
      off.clear();
      if (!only) all.forEach(a => a !== k && off.add(a));
      applyAreas();
    }});
  }});
  network.on('doubleClick', p => {{
    const n = p.nodes.length && nodes.get(p.nodes[0]);
    if (n && n.file) window.open(n.file, '_blank');
  }});

  // ----- forces -----
  const $ = id => document.getElementById(id);
  const start = Object.fromEntries(nodes.get().map(n => [n.id, {{ x: n.x, y: n.y }}]));
  const labels = Object.fromEntries(nodes.get().map(n => [n.id, n.label]));
  const val = id => parseFloat($('f-' + id).value);
  function settings() {{
    const solver = $('f-solver').value;
    const rep = val('repulsion');
    const common = {{
      centralGravity: val('central'), springLength: val('springLength'),
      springConstant: val('springConstant'), damping: val('damping'), avoidOverlap: val('overlap'),
    }};
    return {{
      solver,
      [solver]: {{ ...common, gravitationalConstant: solver === 'barnesHut' ? -rep * 40 : -rep }},
      areaPullLength: val('pull'),
      pinAreaHubs: $('f-pin').checked,
    }};
  }}
  function setRun(on) {{
    $('f-run').checked = on;
    const s = settings();
    network.setOptions({{ physics: {{ enabled: on, solver: s.solver, [s.solver]: s[s.solver],
      stabilization: {{ enabled: false }} }} }});
  }}
  function applyForces() {{
    document.querySelectorAll('#sg-forces input[type=range]').forEach(r =>
      $('o-' + r.id.slice(2)).textContent = r.value);
    edges.update(edges.get({{ filter: e => e.kind === 'pull' }}).map(e => ({{ id: e.id, length: val('pull') }})));
    setRun(true);
  }}
  document.querySelectorAll('#sg-forces input[type=range]').forEach(r => r.addEventListener('input', applyForces));
  $('f-solver').addEventListener('change', applyForces);
  $('f-run').addEventListener('change', e => setRun(e.target.checked));
  $('f-pin').addEventListener('change', e => {{
    const pin = e.target.checked;
    nodes.update(nodes.get({{ filter: n => n.kind === 'area' }}).map(n => {{
      const p = pin ? start[n.id] : network.getPosition(n.id);
      return {{ id: n.id, x: p.x, y: p.y, fixed: {{ x: pin, y: pin }} }};
    }}));
  }});
  $('s-labels').addEventListener('change', e => nodes.update(
    nodes.get({{ filter: n => n.kind === 'tool' || n.kind === 'keyword' }})
      .map(n => ({{ id: n.id, label: e.target.checked ? labels[n.id] : '' }}))));
  const showEdges = (kind, on) => edges.update(
    edges.get({{ filter: x => x.kind === kind }}).map(x => ({{ id: x.id, hidden: !on }})));
  $('s-links').addEventListener('change', e => showEdges('link', e.target.checked));
  $('s-area').addEventListener('change', e => showEdges('area', e.target.checked));
  $('b-stab').addEventListener('click', () => {{ setRun(true); network.stabilize(300); }});
  $('b-reset').addEventListener('click', () => {{
    setRun(false);
    nodes.update(Object.entries(start).map(([id, p]) => ({{ id, x: p.x, y: p.y }})));
    network.fit();
  }});
  $('b-fit').addEventListener('click', () => network.fit());
  $('b-copy').addEventListener('click', e => {{
    navigator.clipboard.writeText(JSON.stringify(settings(), null, 2));
    e.target.textContent = 'Copied';
    setTimeout(() => e.target.textContent = 'Copy settings', 1200);
  }});
}})();
</script>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("company", help="folder name under evidence/")
    args = parser.parse_args()
    g = build(args.company)
    out = ROOT / "evidence" / args.company / "skill-graph.html"
    out.write_text(render(g, args.company), encoding="utf-8")
    kinds = [d["kind"] for _, d in g.nodes(data=True)]
    print(
        f"{out.relative_to(ROOT)}: {kinds.count('project')} projects, {kinds.count('tool')} tools, "
        f"{kinds.count('keyword')} keywords, {g.number_of_edges()} edges"
    )


if __name__ == "__main__":
    main()
