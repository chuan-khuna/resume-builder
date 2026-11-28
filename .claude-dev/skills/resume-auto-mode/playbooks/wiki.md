# Wiki playbook

Maintain `wiki/`: a knowledge base the LLM writes from the sources the user drops into
`wiki/raw/`. Knowledge is compiled once into `wiki/notes/` and kept current, so each source and
each question makes the wiki richer.

Read `wiki/CLAUDE.md` first: the layout, the note format, the citation, link and contradiction
rules, and the log format. Every step below follows it.

Never edit, rename or delete anything in `wiki/raw/`. Never read or ingest the repo-root
`raw/`: the wiki is committed, and `raw/` holds client names and credentials. Follow
"Sensitive data" in `wiki/CLAUDE.md` in every note and log line. Never use a wiki note as
evidence for the resume.

## Pick the operation

Take it from the user's message: `ingest`, `query` or `lint`. With no operation, run
`uv run scripts/wiki.py pending`: ingest if anything is pending, else ask.

## Ingest

One source at a time, with the user in the loop, unless the user asks for a batch.

1. **Pick the source.** Take the file from the message, or the oldest from
   `uv run scripts/wiki.py pending`. If the user pasted content or a URL instead, save it to
   `wiki/raw/<yyyy-mm-dd>-<slug>.md` first (today's date), with the URL at the top. Name the
   file by its topic, never by a client or private name. `wiki/raw/` is committed: if the
   source is private (a call transcript, an internal doc, anything from the user's job), do
   not save it; ask whether to keep its lesson in a note with `sources: []`, as
   "Sensitive data" in `wiki/CLAUDE.md` says.
2. **Read it** in full. For a PDF over 20 pages, read it in page ranges. For images it links,
   read the text first, then view the images that matter.
3. **Discuss.** Tell the user the 3–5 key takeaways and what they would change in the wiki:
   new notes, notes to update, claims that contradict existing notes. Ask what to emphasise.
   Stop until the user answers.
4. **Read the wiki.** Read `notes/index.md`, then every note the source touches.
5. **Write the notes.**
   - A `source` note, slug matching the raw file's, `sources:` naming the raw file.
   - Each `entity`, `concept` or `topic` note the source changes: add its claims with
     citations, update `updated:` and `sources:`, and revise the summary paragraph if the
     view changed. Create a note for an entity or concept that two or more notes now mention.
   - Record each contradiction as the schema says; never overwrite an older claim silently.
   - Link first mentions both ways, so no new note is an orphan.
   - Leave out every sensitive detail, as "Sensitive data" in `wiki/CLAUDE.md` lists. A private
     source gives its lesson, not its names.
6. **Update `notes/index.md`**: add every new note, refresh changed summaries and dates.
7. **Log.** `uv run scripts/wiki.py log ingest "<source title>"` with a `--line` for the
   source, the notes created, the notes updated and any contradiction.
8. **Lint.** Run `uv run scripts/wiki.py lint` and fix every error, sensitive terms first.
   Then read each note you touched for client and person names the script cannot know.
   _Done when_ lint has no errors and the source no longer appears in `pending`.

## Query

1. **Find.** Read `notes/index.md`, then the notes it points to. Follow links one or two hops.
   Read a raw file only when a note's citation is not enough.
2. **Answer** with citations to notes (`[[slug]]`) and raw files. Pick the form that fits: prose,
   a comparison table, a chart, a slide outline. Say plainly what the wiki does not cover,
   and suggest a source that would.
3. **File it** when the answer is worth keeping: a comparison, an analysis, a new connection.
   Ask the user, then write an `answer` note, link it from the notes it drew on, and add it to
   the index. Skip filing for a quick lookup.
4. **Log.** `uv run scripts/wiki.py log query "<question>"` with a `--line` naming the notes
   read and the note filed, if any. Then lint, if you filed a note.

## Lint

1. **Run the checks.** `uv run scripts/wiki.py lint`. Fix every error.
2. **Read for what a script cannot see.** Read the index and the notes, and list:
   - sensitive details the script cannot see: client, colleague or recruiter names, exact
     client figures, private hosts;
   - contradictions between notes not yet flagged;
   - claims a newer source has superseded;
   - orphans from the script's warnings, and where each should be linked from;
   - entities and concepts mentioned in several notes with no note of their own;
   - missing cross-references; summaries that no longer match their note;
   - gaps a new source or a web search could fill, and questions worth asking next.
3. **Report** the list to the user, most important first. Apply the fixes the user approves.
4. **Log.** `uv run scripts/wiki.py log lint "<summary>"` with a `--line` per fix.
   _Done when_ lint has no errors and the user has seen the report.

## Change the schema

When the user changes how the wiki works, or a convention proves wrong, edit `wiki/CLAUDE.md`
and this skill together, and log it with `log schema`.

## Learn

Apply [`../references/learning.md`](../references/learning.md). Typical lessons here:
what the user wants emphasised, which note types or sections they use, how much to ask before
writing. A wiki convention goes into `wiki/CLAUDE.md`.

## Completion

Every touched note follows `wiki/CLAUDE.md`, `notes/index.md` lists every note, the day's log
has an entry for the operation, `scripts/wiki.py lint` reports no errors (including no
sensitive terms), no note holds a detail from the repo-root `raw/`, and nothing in `wiki/raw/`
changed.
