# raw/

Sources for the wiki: articles, papers, job ads, transcripts, notes, data files. Drop a file
here as `<yyyy-mm-dd>-<slug>.<ext>`, then run `/resume-builder:resume-auto-mode wiki ingest <file>`.

Immutable: the LLM reads these files and never edits, renames or deletes them. This folder is
committed and pushed, so it holds public sources only: never a private file such as a call
transcript, an internal doc or anything from your job. See "Sensitive data" in
`wiki/CLAUDE.md`.
