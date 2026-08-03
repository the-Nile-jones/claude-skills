---
name: document-mind-map
description: >-
  Compress a document (PDF, paper, long markdown, chapter, spec, meeting notes)
  into a hierarchical MIND MAP so Nile can SEE its shape — one core idea, branches,
  the non-obvious cross-links, and three questions the document never answers. Runs
  IN-CHAT by default (fast, throwaway); saves a portable `.md` to the vault only when
  Nile asks ("save this"). Use this WHENEVER he wants to see the shape/structure of a
  document — "mind-map this", "map out this PDF/paper", "what's the shape of this
  argument", "I can't tell what's in the middle of this", "I can't see the structure
  of this", or hands over a long doc he needs to grasp fast rather than read linearly.
  NOT for: a prose summary of any length (a map is a navigable hierarchy, not running
  prose); a plain inline outline/TOC; a step-by-step FLOWCHART of a process (a map is
  hierarchical, not sequential); a code-architecture diagram; or when he wants the full
  text read, not compressed. Compression loses nuance — the map says where to look, it
  does not do the looking.
---

# document-mind-map

Conjure the shape of a document so Nile can find the middle he keeps losing. Stolen from a
claude.ai mind-map skill; the charm of the original is that it **costs one step, so you stop
rationing it** — keep that. Default output is an **in-chat nested outline you can throw away**;
persistence is opt-in. (Provenance + the full 10×10× review: vault `KB/Claude/document-mind-map skill — Source Article + RMA-DMA Review (2026-07-01).md`.)

## The 3 non-negotiables (this IS the skill)
1. **One core idea at the center**, everything ladders up to it. *(Exception: a genuinely multi-topic doc — survey, anthology — has no single thesis; map it as a **forest** with a scope label and N sibling centers. Never fabricate a thesis a survey doesn't assert.)*
2. **Flag the non-obvious cross-branch links** — connections the headings don't reveal. This is where insight hides.
3. **End with the questions the document never answers.** This is the payload — it turns the map from a table of contents into a starting point for thinking. Never drop it. (QC below.)

## Default flow (in-chat, lean)
1. **Read the whole thing** first — you can't find the center from the first pages. (Claude's context here holds even a 60-page PDF directly; see Large docs only if it genuinely won't fit.)
2. Find the **core idea** (or forest). Branch supporting points 2–4 levels deep, short labels (~6 words is a guide, not a cap — clarity wins).
3. **Preserve hedges.** If a claim is conditional/probabilistic/contested/single-sourced, keep its qualifier (may / under X / n=1) — never strip it to hit the word budget. A longer honest node beats a short false one.
4. **Mark what you inferred.** Extracted nodes are plain; anything you synthesized — the center of an ambiguous doc, a cross-link, the questions — gets an `[inferred]` marker so Nile can tell the document from your reading.
5. **Cross-branch links** (§ non-negotiable #2): each should name an anchor in *both* branches it joins; if it's your inference rather than stated in the text, mark it `[inferred]`. Don't invent connections that merely sound insightful.
6. Emit as a **nested markdown outline** (readable raw, folds in Obsidian). End with the questions + the one-line caveat.
7. If the input is genuinely unstructured (rambling), **say so and don't force a clean tree** onto mush — that honesty is a feature.

**Doc-type steer (one line, don't ceremony it):** center on what's load-bearing for the type — a paper's *thesis* (methods/results ladder up, no equal corner), a meeting's *decisions/owners/unresolved* (deadlines on nodes that have them), a manual's *goal*.

## The payload — quality control (the crown jewel)
The questions must be **specific, true, and earned** — not filler:
- **Swap test:** if a question would fit under a mind map of a *different* document, it's filler — cut it. Name a specific claim/number/actor/mechanism *from this doc*.
- **Answer-check:** before emitting, confirm the document doesn't actually answer it (scan the source, not a summary). A question the doc answers is an *error* that poisons the map's credibility.
- **Earn it from a gap the map exposed:** a thin/unsupported branch, a hedge you preserved, a cross-link the doc implies but never closes. Note the anchor, e.g. "(from thin branch B)".
- **Flex the count 2–5** by how much the doc genuinely leaves open — never pad to a quota; if only one survives, say so.

Example (paper claiming remote work raises productivity):
- ❌ *"What are the long-term effects of remote work?"* — generic, fits any doc → filler.
- ✅ *"The study measures output over 8 weeks (§4) but calls the effect 'durable' — is 8 weeks evidence of durability, or does the thin longitudinal branch hide the real question?"* — names the doc's number, ties to a thin branch.

## Source pointers (where they help — not a tax)
Attach a pointer **where the source has a natural anchor** (`p.12` / `§3.2` / a quoted anchor); **skip it where forcing one just adds noise** (a rambling essay with no structure). Rules that keep pointers from lying:
- **Pointers come from the extraction, never a model's guess.** `pdftotext` marks pages with form-feeds, not "Page N" — so page numbers must be carried mechanically (per-page extraction with an injected `[[PAGE n]]` tag), never counted by a model over a long doc (it drifts, worst in the middle you care about).
- **A quoted verbatim anchor** (`¶ "…"`) is the one self-verifying pointer — the default for page-less inputs (pasted docs, markdown, URLs). Use `§`/heading-path/line-number for structured-but-page-less docs. Never put `p.N` on an input that has no pages.
- **Synthesized nodes are exempt** — the core idea and cross-links span the doc; give them `(synthesis)` or a range (`pp.11-13`), never a fake single-page cite.
- If you can't locate a node's anchor in the text, downgrade to `(approx)` — a wrong pointer is worse than a missing one.

## Large docs
Default and only path: **read it directly** — Claude's context here handles dozens of pages. ⛔ The former Qwen structure-extraction pre-pass for oversized sources is **REPEALED (2026-07-31**, with all of BICAMERAL); if a source genuinely won't fit, chunk it and read the chunks yourself. The old text already warned "never from Qwen's summary — that's where hedges and answers vanish"; the repeal generalised that warning after Qwen returned a confident `none` on 3 of 5 dense documents. For a PDF, extract text first (the `pdf` skill / `pdftotext`) preserving page boundaries — **do not install an extractor unprompted; if it's missing, print the one install command and stop.** For a **private/authenticated** URL, fetch locally — don't route private content through a cloud fetch tool.

## Optional Mermaid garnish
If Nile wants the GitHub-native picture, add a Mermaid `mindmap` block of the **top ~2 levels only** (it gets unreadable deeper). Caveats: Mermaid `mindmap` is whitespace-driven and treats `()[]{}` as shape syntax — wrap any label with special chars (incl. source pointers) in `"double quotes"` rather than stripping. Whether it renders natively depends on the installed Obsidian's Mermaid version — **unverified on this install; verify once** and fall back to the outline if it parse-errors. (Markmap is **not installed** here, so the outline renders as plain foldable markdown, not an interactive Markmap — don't claim otherwise.)

## Opt-in SAVE (only when Nile asks "save this")
Route the write through `scripts/emit_map.py` — it owns the mount-liveness check (non-empty vault dir), deterministic filename (`YYYY-MM-DD--<slug>--<source-hash>.md`, stable source-date), full house frontmatter, idempotency (skip/refresh if it already exists), and atomic write + read-back. Determinism lives in that script, not here.
- **Route by content sensitivity:** default to your general/technical notes. ⭐ **A map of a sensitive document is exactly as sensitive as the document** — the compression does not launder it. So a map of private material goes wherever that material already lives, **confirm before saving, and never index it into a shared or cloud-backed memory layer.**
- **Wire it into the graph:** on save, add `related: [[…]]` wikilinks + a `## Related notes` block pointing at vault notes the branches touch (reuse the cross-link detection, aimed outward) — so the map isn't an island.
- **Route the payload (offer, don't auto-fire):** offer each open question as a Todoist capture; flag a cross-branch link that recurs across maps as an atom candidate (Neo4j via `atom-cypher-safe`). Your Shadow Offload Rule — don't let the cleverest output die in a file.

## Report back
Where it landed (or "shown in chat, not saved"), the core idea in one line, the questions, and any spot too unstructured to map cleanly.

## Deferred (not built — add only if the happy path proves too small)
Branch-expand into linked child sub-maps · multi-doc / comparison "diff map" · a `Mind Maps/_index.md` MOC · source-hash staleness detection · a shallow/deep depth knob. All flagged by the completeness pass; none earns its complexity yet.
