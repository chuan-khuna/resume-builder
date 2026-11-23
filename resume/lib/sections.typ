// Prints the sections listed in data "sections", in order. Each layout passes
// its own `section(title, body)` wrapper and, optionally, a tuned `entry`.

#import "data.typ": data, shown
#import "style.typ": entry as default-entry, dark-warm

#let render-sections(section, entry: default-entry) = {
  let render = (
    skills: () => {
      let skills = data.at("skills", default: ())
      if skills.len() > 0 {
        section("Skills", grid(
          columns: (auto, 1fr),
          column-gutter: 1.4em,
          row-gutter: 0.85em,
          ..skills.map(s => (text(weight: "medium", fill: dark-warm, s.category), s.items.join(", "))).flatten(),
        ))
      }
    },
    experiences: () => {
      let xs = shown(data.at("experiences", default: ()))
      if xs.len() > 0 {
        section("Experience", xs.map(e => entry(e.jobTitle, time: e.time, description: e.company,
          list(..e.bullets.map(b => if "label" in b [*#b.label*: #b.text] else [#b.text])))).join())
      }
    },
    projects: () => {
      let xs = shown(data.at("projects", default: ()))
      if xs.len() > 0 {
        section("Projects", xs.map(p => entry(p.title, time: p.time,
          description: p.at("description", default: none), url: p.at("url", default: none),
          list(..p.bullets))).join())
      }
    },
    educations: () => {
      let xs = shown(data.at("educations", default: ()))
      if xs.len() > 0 {
        section("Education", xs.map(e => entry(e.degree, time: e.time, description: e.institution,
          list(..e.at("details", default: ())))).join())
      }
    },
    activities: () => {
      let xs = shown(data.at("activities", default: ()))
      if xs.len() > 0 {
        section("Activities", xs.map(a => entry(a.title, time: a.time,
          description: a.at("description", default: none), url: a.at("url", default: none),
          list(..a.at("details", default: ())))).join())
      }
    },
    interests: () => {
      let xs = data.at("interests", default: ())
      if xs.len() > 0 { section("Interests", list(..xs)) }
    },
  )

  for name in data.at("sections", default: ("skills", "experiences", "projects", "educations", "activities")) {
    assert(name in render, message: "unknown section " + repr(name) + " in \"sections\"")
    render.at(name)()
  }
}
