// Rail variant of classic.typ: section headings hang in a narrow left column
// and all content sits in a narrower right column. Same data and versions;
// shared data and style live in lib/.
//
//   mise run build rail                 -> build/base/rail.pdf
//   mise run version <slug> rail        -> build/<slug>/rail.pdf

#import "../lib/data.typ": data
#import "../lib/style.typ": setup, header, summary, entry, serif, ink, rule
#import "../lib/sections.typ": render-sections

// Tighter spacing than classic.typ: the narrower column wraps more lines.
#show: setup.with(leading: 0.62em, list-spacing: 0.52em)

// Rail geometry: heading column + gutter; content takes the rest.
#let rail = 24mm
#let gutter = 5mm

// Section headings: Geist Serif in the rail. Cap-height top edges line the heading
// up with the first line of its content.
#show heading.where(level: 2): it => text(font: serif, size: 13pt, weight: "regular",
  fill: ink, top-edge: "cap-height", it.body)

// Hang content in the right column; the rail stays empty when no label is given.
#let hang(label, body) = grid(columns: (rail, 1fr), column-gutter: gutter, label, body)

#header(data.header)

#if summary(data.header) != none {
  v(1em)
  hang([], summary(data.header))
}

// A full-width hairline separates sections; the heading hangs in the rail.
#render-sections(
  (title, body) => block(above: 0.9em, below: 0pt, {
    line(length: 100%, stroke: 0.5pt + rule)
    v(0.75em)
    hang(heading(level: 2, title), body)
  }),
  entry: entry.with(below: 0.95em),
)
