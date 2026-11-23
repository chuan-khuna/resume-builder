#!/usr/bin/env bash
# Measure a built resume for /review-resume. Prints a plain-text report;
# every number in a review must come from here or another command, not an estimate.
#
#   bash .claude-dev/skills/review-resume/measure.sh [slug] [template]   (from the repo root)
#   slug: "base" (resume/data/resume.yml) or a folder in resume/versions/   default: base
#   template: a file in resume/templates/, without .typ               default: classic
#
# Needs: mise (typst, bun), pdftotext/pdfinfo/pdffonts on PATH (brew install poppler).
# Runs in resume/: every path below is relative to it.
set -uo pipefail

slug=${1:-base}
tpl=${2:-classic}
cd "$(git rev-parse --show-toplevel)/resume" || exit 1

input=()
[ "$slug" != base ] && input=(--input "version=$slug")
pdf="build/$slug/$tpl.pdf"

section() { printf '\n== %s\n' "$1"; }

# ---------- Build (also runs the page-count check) ----------
section "Build: $pdf"
if [ "$slug" = base ]; then task=(build "$tpl"); else task=(version "$slug" "$tpl"); fi
if ! out=$(mise run "${task[@]}" 2>&1); then
  echo "BUILD FAILED"; echo "$out" | grep -v '^\[' ; exit 1
fi
echo "ok; page images: $(ls build/"$slug"/"$tpl"-*.png | tr '\n' ' ')"

# ---------- PDF facts ----------
section "PDF"
pdfinfo "$pdf" 2>/dev/null | grep -E '^(Title|Author|Tagged|Pages|Page size):'
grep -ao '/Lang *([^)]*)' "$pdf" | head -1
echo "fonts (name, embedded, unicode map):"
pdffonts "$pdf" 2>/dev/null | awk 'NR>2 {print "  " $1, "emb=" $(NF-4), "uni=" $(NF-2)}'
echo "links:"; grep -ao '/URI *([^)]*)' "$pdf" | sed 's/^/  /'

# ---------- Text extraction (ATS view) ----------
plain=$(pdftotext -enc UTF-8 "$pdf" -)
raw=$(pdftotext -raw -enc UTF-8 "$pdf" -)
layout=$(pdftotext -layout -enc UTF-8 "$pdf" -)

section "Text"
echo "words: $(wc -w <<<"$plain")"
echo "ligature characters (ﬀ ﬁ ﬂ ﬃ ﬄ): $(grep -o '[ﬀﬁﬂﬃﬄ]' <<<"$plain" | wc -l)"
echo "replacement characters (U+FFFD): $(grep -o '�' <<<"$plain" | wc -l)"

section "Skills: stored order (pdftotext -raw)"
sed -n '/^Skills$/,/^[A-Z][a-z]*$/p' <<<"$raw" | sed '1d;$d' | cut -c1-110
section "Skills: by position (pdftotext plain)"
sed -n '/^Skills$/,/^[A-Z][a-z]*$/p' <<<"$plain" | sed '1d;$d' | grep -v '^$' | cut -c1-110

section "Line length (characters, -layout, bullet lines)"
grep '•' <<<"$layout" | sed 's/^ *//; s/ *$//' | awk '{print length}' | sort -n |
  awk '{a[NR]=$1} END {if (NR) print "lines", NR, "median", (NR % 2 ? a[(NR+1)/2] : (a[NR/2] + a[NR/2+1]) / 2), "max", a[NR]}'

section "Wrapped bullets: words on the last line"
awk 'p ~ /^•/ && $0 ~ /^[a-z]/ {print "  " NF " words: " substr($0,1,70)} NF {p=$0}' <<<"$plain"

# ---------- Positions from Typst's own layout ----------
section "Section positions (A4 = 842 pt)"
probe="build/_probe-$tpl.typ"
printf '#include "../templates/%s.typ"\n#context [#metadata(query(heading).map(h => (repr(h.body), h.location().position().y.pt()))) <probe>]\n' "$tpl" > "$probe"
mise exec -- typst eval 'query(<probe>).first().value' --in "$probe" "${input[@]}" --format json 2>/dev/null |
  mise exec -- bun -e '
    const hs = JSON.parse(await Bun.stdin.text());
    for (const [t, y] of hs) console.log(`  ${t.replace(/^\[|\]$/g, "").padEnd(14)} ${y.toFixed(0).padStart(4)} pt  ${(y / 841.89 * 100).toFixed(0)}%`);'
rm -f "$probe"

# ---------- Content facts from the merged data ----------
section "Content"
mise exec -- typst eval '{ import "/lib/data.typ": data; data }' --in "templates/$tpl.typ" "${input[@]}" --format json 2>/dev/null |
  mise exec -- bun -e '
    const d = JSON.parse(await Bun.stdin.text());
    // Only what is printed: entries not hidden, in sections listed in "sections"
    // (default list as in lib/sections.typ).
    const printed = d.sections ?? ["skills", "experiences", "projects", "educations", "activities"];
    const shown = (key) => (printed.includes(key) ? d[key] ?? [] : []).filter((x) => !x.hidden);
    const words = (s) => s.trim().split(/\s+/).length;
    const hd = d.header;
    console.log("sections:", printed.join(", "), "| maxPages:", d.maxPages ?? 1);
    console.log("summary words:", words([hd.headline, hd.introduction].filter(Boolean).join(" ")));
    let bullets = [];
    for (const e of shown("experiences")) {
      const b = e.bullets.map((x) => (typeof x === "string" ? x : `${x.label}: ${x.text}`));
      bullets.push(...b);
      console.log(`job "${e.jobTitle}" (${e.time}): ${b.length} bullets, words ${b.map(words).join(",")}`);
    }
    for (const p of shown("projects")) bullets.push(...p.bullets);
    const withNum = bullets.filter((b) => /\d/.test(b.replace(/\b(19|20)\d\d\b/g, "")));
    console.log(`bullets with a number (years excluded): ${withNum.length} of ${bullets.length}`);
    // Gaps between education end and work, and between jobs.
    const mon = { Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11 };
    const parse = (s) => { const m = s.trim().match(/^(?:([A-Z][a-z]{2}) )?(\d{4})$/); return m ? +m[2] * 12 + (m[1] ? mon[m[1]] : 0) : null; };
    const spans = [...shown("experiences").map((e) => ["job " + e.jobTitle, e.time]), ...shown("educations").map((e) => ["education", e.time])]
      .map(([n, t]) => { const [a, b] = t.split(" - "); return { n, a: parse(a), b: b === "Present" ? 1e9 : parse(b) }; })
      .filter((s) => s.a != null).sort((x, y) => x.a - y.a);
    for (let i = 1; i < spans.length; i++) {
      const gap = spans[i].a - spans[i - 1].b;
      if (gap > 6) console.log(`GAP ${Math.floor(gap / 12)}y ${gap % 12}m between ${spans[i - 1].n} and ${spans[i].n}`);
    }
    const dates = [...shown("experiences"), ...shown("projects"), ...shown("educations"), ...shown("activities")].map((x) => x.time);
    const yearOnly = dates.filter((t) => /(^|- )\d{4}/.test(t));
    if (yearOnly.length) console.log("dates without a month:", yearOnly.join(" | "));
    const noUrl = shown("projects").filter((p) => !p.url).map((p) => p.title);
    if (noUrl.length) console.log("projects without a link:", noUrl.join(" | "));'

# ---------- Contrast of every colour in lib/style.typ, on white ----------
section "Contrast on white (WCAG 2.2; AA text >= 4.5, AAA >= 7)"
grep -o '#let [a-z-]* = rgb("#[0-9a-fA-F]\{6\}")' lib/style.typ | sed 's/#let \([a-z-]*\) = rgb("\(#[0-9a-fA-F]*\)")/\1 \2/' |
  mise exec -- bun -e '
    const L = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255)
      .map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4))
      .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
    for (const line of (await Bun.stdin.text()).trim().split("\n")) {
      const [name, hex] = line.split(" ");
      const r = 1.05 / (L(hex) + 0.05);
      console.log(`  ${name.padEnd(10)} ${hex}  ${r.toFixed(2).padStart(5)}:1  ${r >= 7 ? "AAA" : r >= 4.5 ? "AA" : "below AA (ok only if decorative)"}`);
    }'
echo "(also check colours set inline, e.g. lighten(), in lib/ and templates/)"
