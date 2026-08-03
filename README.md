# claude-skills

Skills I wrote for [Claude Code](https://claude.com/claude-code) while running a personal
infrastructure stack — backups, MCP servers, a knowledge base, a self-hosted dashboard.

They are not tutorials. Each one exists because something broke in a specific way and I wanted
the fix to fire again without my having to remember it.

## The through-line

Most of these are variations on one problem: **an acknowledgement is not an effect.**

A backup script exits 0 because `tar` didn't crash — not because the archive has anything in it.
An API returns `HTTP 200` for a delete that deleted nothing. A search returns zero results because
the query was malformed, and that renders identically to "there is nothing there."

Systems that fail this way stay broken for weeks, because nothing reports being broken. The
skills below are mostly instruments for telling those two states apart.

## What's here

| Skill | What it does |
|---|---|
| **zero-as-answer** | Audits code for the silent-failure family: places where an *absence* is treated as a *result*, so "I looked and found nothing" and "I couldn't look" produce the same output. |
| **atom-cypher-safe** | Safe write-layer for a Neo4j knowledge graph. Gates destructive Cypher, enforces schema, dedups before insert, and read-back-verifies every write. |
| **diverge** | Fans out context-isolated agents under different named cognitive frames, then converges to a shortlist plus the traps. For when the first three answers all sound like the same answer. |
| **handoff** | Produces a session handoff another agent (or a later you) can actually act on — state, open threads, and what was verified vs. assumed. |
| **skill-scout** | Recon-and-triage for external skill sources. Dedups every candidate against what you already have *first*, then reports new / already-covered / diminishing-returns. |
| **prompt-forge** | Turns a rough task into a paste-ready prompt. Best for prompts headed somewhere else — a fresh session, a subagent, another machine. |
| **what-should-i-automate** | Finds the repetitive work worth automating, and — more usefully — the work that isn't. |
| **document-mind-map** | Turns a long document into a navigable structural map instead of a summary. |
| **notebooklm-bulk-label** | Bulk source labelling / reorganisation for NotebookLM corpora. |

Also mine, in its own repo: **[job-scout](https://github.com/the-Nile-jones/job-scout)** — pulls
job postings from Greenhouse/Lever/Ashby + RemoteOK + HN "Who is hiring", and refuses to merge a
failed lookup into "no jobs found."

## Install

Drop a skill directory into `~/.claude/skills/`:

```bash
git clone https://github.com/the-Nile-jones/claude-skills
cp -r claude-skills/skills/zero-as-answer ~/.claude/skills/
```

Claude Code picks it up on the next session. Each skill is a single `SKILL.md` (a couple have
supporting files); there is nothing to build and no dependencies to install.

## What is deliberately not here

- **Third-party skills.** My local setup also runs skills from
  [obra/superpowers](https://github.com/obra/superpowers), Anthropic, Trail of Bits, Cloudflare
  and others. Those are someone else's work — credited and linked, not republished.
- **Skills that carry private specifics.** Several of mine are wired to my own paths, task IDs and
  documents. They stay local rather than get half-scrubbed into something misleading.

## License

MIT — see [LICENSE](LICENSE). Use them, fork them, rewrite them.
