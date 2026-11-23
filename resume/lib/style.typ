// Shared look for every layout. Kami (紙) rules: warm neutrals plus one
// ink-blue accent, weights 400/500 only, no italic; type size and space carry
// the hierarchy, and hairlines appear only where they separate regions.

#import "data.typ": data

// ---------- Fonts and palette ----------

// Fonts live in fonts/ (mise.toml sets TYPST_FONT_PATHS and ignores system fonts):
// Geist for the body, Geist Serif for the name and section headings (SIL OFL).
// Override to try another pairing: --input sans="…" --input serif="…"
#let sans = sys.inputs.at("sans", default: "Geist")
#let serif = sys.inputs.at("serif", default: "Geist Serif")   // name and section headings

// Body size: the "size" input if given; otherwise 8.8pt.
#let body-size = float(sys.inputs.at("size", default: "8.8")) * 1pt

#let ink = rgb("#141413")        // near-black body text
#let dark-warm = rgb("#3d3d3a")  // secondary text
#let olive = rgb("#504e49")      // company / institution lines
#let stone = rgb("#6b6a64")      // dates, metadata, bullet markers
#let rule = rgb("#e8e6dc")       // hairlines
#let accent = rgb("#1b365d")     // ink-blue, the only accent

// ---------- Helpers ----------

// Date ranges take an en dash: "Jul 2022 - Present" -> "Jul 2022 – Present".
#let range(t) = t.replace(" - ", " \u{2013} ")

// "https://github.com/x/" -> "github.com/x"
#let short-url(url) = url.trim("https://", at: start).trim("/", at: end)

// ---------- Page setup ----------

// Apply with `#show: setup` (or `setup.with(...)` to tighten spacing).
// Also fails the build when the resume runs past "maxPages" (default 1).
#let setup(leading: 0.68em, list-spacing: 0.62em, body) = {
  set document(title: data.header.name + "'s Resume", author: data.header.name)
  set page(paper: "a4", margin: (x: 15mm, y: 13mm), footer-descent: 40%,
    // Page numbers only when the resume runs past one page.
    footer: context {
      let total = counter(page).final().first()
      if total > 1 {
        set text(size: 8.5pt, fill: stone)
        data.header.name
        h(1fr)
        counter(page).display() + " / " + str(total)
      }
    })
  set text(font: sans, size: body-size, fill: ink, lang: "en", hyphenate: false,
    number-width: "tabular")
  set par(justify: false, leading: leading, spacing: 0.8em)
  set list(indent: 0.1em, body-indent: 0.6em, spacing: list-spacing,
    marker: text(fill: stone, sym.bullet))
  set strong(delta: 100)   // regular 400 -> medium 500, never bold
  show link: set text(fill: accent)

  body

  context {
    let pages = counter(page).final().first()
    let max = data.at("maxPages", default: 1)
    assert(pages <= max, message: "resume is " + str(pages) + " pages; it must fit on " + str(max) + ". Trim content, hide entries, or raise \"maxPages\".")
  }
}

// ---------- Building blocks ----------

// Title (+ short URL) left, date right, on one shared baseline;
// organisation below in olive (no italic).
#let entry(title, time: none, description: none, url: none, below: 1.15em, body) = block(breakable: false, below: below, {
  block(below: 0.5em, {
    text(size: 10.3pt, weight: "medium", title)
    if url != none { h(0.55em); text(size: 8.6pt, link(url, short-url(url))) }
    h(1fr)
    if time != none { text(size: 9pt, fill: stone, range(time)) }
  })
  if description != none { block(below: 0.7em, text(size: 9.4pt, fill: olive, description)) }
  body
})

// Name, job title, and one contact line. Explicit stack gaps, because
// paragraph spacing would scale with the 26pt name.
#let header(hd) = stack(
  dir: ttb,
  text(font: serif, size: 26pt, weight: "regular", tracking: -0.2pt, top-edge: "cap-height", hd.name),
  7pt,
  text(size: 11pt, weight: "medium", fill: accent, hd.jobTitle),
  6pt,
  text(size: 9pt, fill: dark-warm, {
    let parts = (hd.location, link("mailto:" + hd.email, hd.email))
    if "github" in hd { parts.push(link(hd.github, "github.com/" + hd.at("githubName", default: ""))) }
    if "website" in hd { parts.push(link(hd.website, short-url(hd.website))) }
    parts.join(h(0.6em) + text(fill: stone.lighten(35%), sym.bar.v) + h(0.6em))
  }),
)

// Optional medium-weight headline, then the introduction; none without one.
#let summary(hd) = if "introduction" in hd [#if "headline" in hd [#strong(hd.headline) ]#hd.introduction]
