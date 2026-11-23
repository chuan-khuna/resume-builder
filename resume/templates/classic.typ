// One-column resume (Kami styling): Geist Serif headings over a hairline,
// title left / date right. Shared data and style live in lib/.
//
//   mise run build                      -> build/base/classic.pdf
//   mise run version 2026-jul-dev       -> build/2026-jul-dev/classic.pdf

#import "../lib/data.typ": data
#import "../lib/style.typ": setup, header, summary, serif, ink, rule
#import "../lib/sections.typ": render-sections

#show: setup

// Section headings: Geist Serif over a quiet full-width hairline.
#show heading.where(level: 2): it => block(above: 1.9em, below: 0.95em, sticky: true, breakable: false, {
  text(font: serif, size: 14.5pt, weight: "regular", fill: ink, it.body)
  v(0.45em, weak: true)
  line(length: 100%, stroke: 0.5pt + rule)
})

#header(data.header)

#if summary(data.header) != none {
  v(0.6em)
  summary(data.header)
}

#render-sections((title, body) => { heading(level: 2, title); body })
