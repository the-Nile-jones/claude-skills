---
name: handoff
description: >-
  Generate a structured continuity handoff on demand — before a /clear, at session end, when handing to a fresh agent/subagent, or when passing work to the other machine (aiserver↔gcloud). Picks the right destination + format automatically. Use when Nile says "hand off", "write a handoff", "/handoff", "prep for /clear", "pass this to the gcloud box / aiserver", or "summarize this session so the next one can continue". Inherits the repeatable-generator + suggested-skills + reference-don't-duplicate + redaction discipline from the mattpocock/skills handoff idea, re-derived in Nile's richer format. On-demand: suggest it, don't auto-fire.
---

# handoff — Structured Continuity Generator

Generate a handoff doc that lets the *next* context — a fresh session here, a subagent, or the other machine — pick up exactly where this one left off, with no re-derivation. Your handoffs were hand-authored ad-hoc; this makes generation deterministic, complete, and consistently formatted.

It does **not** replace the existing continuity layers — it's the missing *generator* that writes into them correctly:
- **`hot_cache.md`** (`~/Exocortex/`) — same-machine, session→next-session rolling cache (auto-maintained; this skill updates its CONTINUE-FROM block, never a parallel file).
- **`gcloud-handoff/`** (`~/.claude/`) — cross-machine peer transfer, ingestion-ready memory-entry blocks, archived.
- **capture buffer** — inline→canon merge (separate concern; reference it, don't duplicate it).

## Step 0 — pick the mode (destination decision tree)

Infer from context; ask only if genuinely ambiguous.

```
Who picks this up next?
├─ The next session on THIS machine (before /clear, or session end)
│     → MODE A: update hot_cache CONTINUE-FROM
├─ The OTHER machine (aiserver ↔ gcloud satellite)
│     → MODE B: write ~/.claude/gcloud-handoff/<ISO>Z-handoff.md (memory-block format)
└─ A throwaway fresh agent / subagent / external paste (no persistence needed)
      → MODE C: write to a temp path ($TMPDIR or /tmp), report the path
```

If Nile passed an argument, treat it as **"what the next session will focus on"** and tailor the whole doc to that (lead with what's relevant to that focus; drop unrelated detail).

## Universal rules (every mode)

These are the quality layer — they apply regardless of destination:

1. **Lead with the `role:` line.** State the role the next context should assume (`executor | architect | researcher | auditor`, per SOUL.md). Default `executor` unless the work implies otherwise.
2. **Reference, don't duplicate.** If something is already captured — a Todoist task (give the ID), a Drive doc, a KB note, the capture buffer, a commit, a memory file — **link/cite it by path or ID, do not re-paste its content.** The handoff is a pointer-map + the in-flight state that isn't written down anywhere else yet. This is the anti-bloat rule; a handoff that re-paginates existing artifacts is a bad handoff.
3. **Suggested skills / next actions.** Include a short section naming the skills the next context should invoke and the immediate next steps — the forward-pointer. (e.g. "→ resume with `/change-discipline` on the pending vault sweep; the dry-run is at …".)
4. **Redact secrets — hard rule.** Never write token/secret *values*. Reference GSM secrets by NAME only (`YNAB_ACCESS_TOKEN`), never the value. No API keys, passwords, or PII (this is outward-portable; apply the secrets + sensitive-data discipline). Scrub before write.
5. **State the in-flight state honestly.** What's done, what's mid-flight, what's blocked and on what. If a background task is running, say so and where its output lands. If something's unverified, mark it.
6. **Timestamp + one-line.** Open with a one-line "what this session did" so the reader orients in 5 seconds.

## Mode A — next-session (same machine) → hot_cache CONTINUE-FROM

Update `~/Exocortex/hot_cache.md`: replace/refresh the `### ⮕ CONTINUE-FROM` block near the top (keep it TIGHT — the file is a ~500-word rolling cache; older arcs roll to `hot_cache_archive.md` via `hotcache-archive-retain.py`, don't fight that). Match the existing shape:

```
### ⮕ CONTINUE-FROM (<YYYY-MM-DD> — <one-line focus>) — READ FIRST
**role: <role>.**
- <in-flight state, one bullet each — reference task IDs / paths, don't paste>
- **Suggested next:** <skills to invoke + immediate steps>
- **Running bg (check if no report):** <any background agents + where output lands>
```

Don't bloat hot_cache — if there's heavy detail, it belongs in a Todoist task/Drive doc that you *reference* here. Update the file's `# Last updated:` header line too.

## Mode B — cross-machine → gcloud-handoff (ingestion-ready)

Write `~/.claude/gcloud-handoff/<ISO8601-compact>Z-handoff.md` (e.g. `20260615T161748Z-handoff.md`). **Match the exact existing schema** — the receiving machine's boot-sweep (`cortex-inbox-check.sh`) flags it and the next session ingests→integrates→archives it, so the format must parse:

```
# Handoff — <short title of what this session accomplished>

**One-line:** <2-3 sentence summary>

**role:** <role>

---

## Memory entry 1 (<project|reference|feedback|user>)
- **name:** <kebab-slug>
- **description:** <one-line, used for recall relevance>
- **type:** <project|reference|feedback|user>

<self-contained body — for cross-machine, entries ARE self-contained (the peer may not have your local files), but still reference shared canon (Drive/Todoist IDs) the peer can also reach.>

---
## Memory entry 2 (...)
...
```

Machine-agnostic: works aiserver→gcloud OR gcloud→aiserver — don't assume which is hub (the aiserver-decommission is in progress; the direction is shifting). Name the source machine in the title. Archive prior handoffs per the existing `archive/` convention only after they're confirmed ingested.

## Mode C — throwaway / fresh agent

Write to `${TMPDIR:-/tmp}/handoff-<ISO>Z.md`, report the path. Use the article's lean shape (one-line + role + state + suggested-skills + references). No persistence, no archive — it's for an agent that needs context once. Still redact.

## Anti-patterns (don't)

- **Don't re-paste what's already written.** Reference task IDs / paths / commits. The buffer, hot_cache, Todoist, Drive, and memory files are the canon — point at them.
- **Don't write a parallel same-machine artifact.** Mode A updates hot_cache; it doesn't create `handoff-local.md`. One continuity surface per machine.
- **Don't break the gcloud-handoff schema.** The peer's ingest expects the memory-entry-block format. Malformed → the next session can't integrate it.
- **Don't leak secrets.** GSM names only, never values. Scrub before write — this artifact is portable and may cross machines.
- **Don't bloat.** A handoff is a pointer-map + in-flight state, not a transcript. If it's getting long, you're duplicating artifacts that should be referenced.

## Provenance

Native re-derivation (inherit→atomize→rebuild) of the `mattpocock/skills` `handoff` idea (surfaced via the Firecrawl best-skills list, 2026-06-15), vetted against Nile's existing 3-layer continuity infra and 3×3×-tested. Inherited from the article: repeatable-generator, suggested-skills forward-pointer, reference-don't-duplicate, redaction, argument-tailoring. Kept from Nile's setup: the `role:` line, memory-entry-block format, hot_cache CONTINUE-FROM convention, gcloud-handoff persistence/archive. 3×3× refinements folded in: same-machine updates hot_cache (no parallel artifact), match the gcloud-handoff schema exactly (ingest safety), machine-agnostic (aiserver-decommission in progress). Composes with `cortex-inbox-check.sh` (boot-sweep) + `hotcache-archive-retain.py` (rolloff).
