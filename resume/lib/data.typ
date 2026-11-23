// Resume data: data/resume.yml, plus an optional version file.
// A version file replaces whole top-level keys (no merging within a section),
// like the Resume Versions in digital-garden-2024.
//
//   --input version=<slug>   -> versions/<slug>/resume.yml

#let base = yaml("../data/resume.yml")
#let version = sys.inputs.at("version", default: none)
#let data = if version == none { base } else { base + yaml("../versions/" + version + "/resume.yml") }

// Entries marked "hidden": true stay in the data but are not printed.
#let shown(entries) = entries.filter(e => not e.at("hidden", default: false))
