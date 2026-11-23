# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.9"]
# ///
"""Plot the distribution of line lengths in built resumes, for review pages.

Reads build/<slug>/<template>.pdf with `pdftotext -layout` and measures, in
characters including spaces:
  - bullet lines: visual lines that start with a bullet (same as measure.sh)
  - summary lines: the paragraph between the contact line and the first heading

Draws horizontal violins (5+ lines) with every line as a dot, the 45-90 comfortable range
shaded and 100 marked, and prints the same numbers as a table.

    uv run review/scripts/line_lengths.py                       # base, classic + rail
    uv run review/scripts/line_lengths.py --slug acme --templates classic
    uv run review/scripts/line_lengths.py -o review/acme-line-length.svg

Build the PDFs first (from resume/: mise run build / mise run version <slug> <template>).
"""

import argparse
import statistics
import sys
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

# Review page palette (review/styles/review.css).
INK, DARK, STONE, RULE, PAPER, ACCENT = "#141413", "#3d3d3a", "#6b6a64", "#e8e6dc", "#faf9f5", "#1b365d"
COMFORT = (45, 90)  # comfortable reading range, characters per line
LIMIT = 100  # beyond this, the eye loses its place on the return sweep
MIN_VIOLIN = 5  # fewer lines than this: dots only, a violin would invent a shape


def line_lengths(pdf: Path) -> dict[str, list[int]]:
    text = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    lines = [line.strip() for line in text.splitlines()]

    bullets = [len(line) for line in lines if line.startswith("•")]

    # Summary: lines after the contact line (the one with the email) up to the first heading.
    summary: list[int] = []
    start = next((i for i, line in enumerate(lines) if "@" in line), None)
    if start is not None:
        for line in lines[start + 1:]:
            if line == "":
                if summary:
                    break
                continue
            summary.append(len(line))
    return {"bullet lines": bullets, "summary lines": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--slug", default="base", help="build/<slug>/ folder (default: base)")
    parser.add_argument("--templates", nargs="+", default=["classic", "rail"], help="templates to compare")
    parser.add_argument("-o", "--output", type=Path, help="SVG path (default: review/<slug>-line-length.svg)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = args.output or ROOT / "review" / f"{args.slug}-line-length.svg"

    groups: list[tuple[str, list[int]]] = []
    for tpl in args.templates:
        pdf = ROOT / "build" / args.slug / f"{tpl}.pdf"
        if not pdf.exists():
            raise SystemExit(f"missing {pdf.relative_to(ROOT)}: build it first")
        for kind, values in line_lengths(pdf).items():
            if values:
                groups.append((f"{tpl.capitalize()} · {kind}", values))

    # Table view: the same numbers as the chart.
    print(f"{'group':<28}{'n':>4}{'min':>6}{'median':>8}{'max':>6}{'> 100':>7}")
    for label, v in groups:
        over = sum(x > LIMIT for x in v)
        print(f"{label:<28}{len(v):>4}{min(v):>6}{statistics.median(v):>8g}{max(v):>6}{over:>7}")

    plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": DARK,
                         "xtick.color": STONE, "ytick.color": DARK, "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(8, 0.75 * len(groups) + 1.3), facecolor=PAPER)
    ax.set_facecolor(PAPER)

    ax.axvspan(*COMFORT, color=RULE, zorder=0)
    ax.text(sum(COMFORT) / 2, len(groups) - 0.35, "comfortable 45–90", ha="center", va="bottom", color=STONE, fontsize=9)
    ax.axvline(LIMIT, color=STONE, lw=1, ls=(0, (3, 3)), zorder=1)
    ax.text(LIMIT + 1.5, len(groups) - 0.35, "100", ha="left", va="bottom", color=STONE, fontsize=9)

    rng = np.random.default_rng(0)  # fixed jitter so the image is stable between runs
    for i, (label, v) in enumerate(reversed(groups)):
        y = i
        if len(v) >= MIN_VIOLIN and len(set(v)) > 1:
            parts = ax.violinplot(v, positions=[y], orientation="horizontal", widths=0.75, showextrema=False)
            for body in parts["bodies"]:
                body.set_facecolor(ACCENT)
                body.set_alpha(0.18)
                body.set_edgecolor("none")
        ax.scatter(v, y + rng.uniform(-0.12, 0.12, len(v)), s=22, color=ACCENT,
                   edgecolors=PAPER, linewidths=1, zorder=3)
        med = statistics.median(v)
        ax.plot([med, med], [y - 0.28, y + 0.28], color=INK, lw=2, solid_capstyle="round", zorder=4)
        ax.text(med, y + 0.32, f"median {med:g}", ha="center", va="bottom", color=DARK, fontsize=8.5, zorder=4)

    ax.set_yticks(range(len(groups)), [label for label, _ in reversed(groups)])
    ax.set_ylim(-0.6, len(groups) - 0.1)
    lo = min(COMFORT[0], min(min(v) for _, v in groups)) - 5
    hi = max(LIMIT, max(max(v) for _, v in groups)) + 8
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Characters per line")
    ax.set_title(f"Line length, build/{args.slug}/", loc="left", color=INK, fontsize=12, pad=14)
    ax.grid(axis="x", color=RULE, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(axis="y", length=0)

    fig.tight_layout()
    fig.savefig(out, format="svg", facecolor=PAPER)
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
